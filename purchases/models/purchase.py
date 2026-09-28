from decimal import Decimal

from django.db import models

from accounting.models import Account
from company.models import Company
from fiscal.models import Tax
from suppliers.models import Supplier


class Purchase(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="purchases",
    )
    date = models.DateField()
    invoice_number = models.CharField(max_length=50)

    # Totales
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    perception_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retention_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.invoice_number} - {self.supplier.name}"

    def calculate_totals(self):
        money = Decimal("0.01")

        # 1) Subtotal Neto Gravado desde las líneas de compra
        self.net_amount = sum(
            (line.quantity * line.unit_price for line in self.lines.all()),
            Decimal("0"),
        ).quantize(money)

        # 2) IVA / Impuestos automáticos desde Tax
        for tax_line in self.taxes.all():
            tax_obj = tax_line.tax
            if tax_obj is None:
                tax_line.amount = Decimal("0")
                tax_line.save(update_fields=["amount"])
                continue

            if tax_line.base_amount <= 0:
                tax_line.base_amount = self.net_amount

            tax_line.amount = (
                tax_line.base_amount * tax_obj.rate / Decimal("100")
            ).quantize(money)
            tax_line.save(update_fields=["base_amount", "amount"])

        # 3) Percepciones automáticas basadas en perfil fiscal del proveedor
        profile = getattr(self.supplier, "tax_profile", None)

        if profile:
            # --- IIBB ---
            is_iibb_agent = getattr(profile, "is_iibb_perception_agent", False)
            iibb_rate = Decimal(str(getattr(profile, "iibb_perception_rate", 0) or "0"))

            if (is_iibb_agent or iibb_rate > 0) and not getattr(profile, "is_iibb_exempt", False):
                iibb_perc, _ = self.perceptions.get_or_create(
                    perception_type="IIBB",
                    defaults={"amount": Decimal("0")},
                )
                if iibb_rate > 0:
                    iibb_perc.amount = (self.net_amount * iibb_rate / Decimal("100")).quantize(money)
                else:
                    iibb_perc.amount = Decimal("0")
                iibb_perc.save()

            # --- IVA ---
            is_iva_agent = getattr(profile, "is_iva_perception_agent", False)
            iva_rate = Decimal(str(getattr(profile, "iva_perception_rate", 0) or "0"))
            afip_cat = getattr(profile, "afip_category", "")

            if is_iva_agent or iva_rate > 0:
                iva_perc, _ = self.perceptions.get_or_create(
                    perception_type="IVA",
                    defaults={"amount": Decimal("0")},
                )
                if iva_rate > 0:
                    iva_perc.amount = (self.net_amount * iva_rate / Decimal("100")).quantize(money)
                elif is_iva_agent and afip_cat == "RI":
                    iva_perc.amount = (self.net_amount * Decimal("0.03")).quantize(money)
                else:
                    iva_perc.amount = Decimal("0")
                iva_perc.save()

        # Recalcular cualquier otra percepción existente
        for p in self.perceptions.all():
            if not profile:
                p.amount = Decimal("0")
                p.save()
                continue

            if p.perception_type == "IIBB":
                iibb_rate = Decimal(str(getattr(profile, "iibb_perception_rate", 0) or "0"))
                if iibb_rate > 0 and not getattr(profile, "is_iibb_exempt", False):
                    p.amount = (self.net_amount * iibb_rate / Decimal("100")).quantize(money)
                else:
                    p.amount = Decimal("0")
                p.save()

            elif p.perception_type == "IVA":
                iva_rate = Decimal(str(getattr(profile, "iva_perception_rate", 0) or "0"))
                if iva_rate > 0:
                    p.amount = (self.net_amount * iva_rate / Decimal("100")).quantize(money)
                elif getattr(profile, "is_iva_perception_agent", False) and getattr(profile, "afip_category", "") == "RI":
                    p.amount = (self.net_amount * Decimal("0.03")).quantize(money)
                else:
                    p.amount = Decimal("0")
                p.save()

            elif p.perception_type == "MUNI":
                p.amount = Decimal("0")
                p.save()

        # 4) Retenciones automáticas basadas en perfil fiscal del proveedor
        for r in self.retentions.all():
            if not profile:
                r.amount = Decimal("0")
                r.save()
                continue

            if r.retention_type == "GAN":
                ganancias_rate = Decimal(str(getattr(profile, "ganancias_retention_rate", 0) or "0"))
                if ganancias_rate > 0 and getattr(profile, "ganancias_status", "") == "INSCRIPTO" and not getattr(profile, "is_ganancias_exempt", False):
                    r.amount = (self.net_amount * ganancias_rate / Decimal("100")).quantize(money)
                else:
                    r.amount = Decimal("0")

            elif r.retention_type == "IVA":
                iva_ret_rate = Decimal(str(getattr(profile, "iva_retention_rate", 0) or "0"))
                iva_total = sum(t.amount for t in self.taxes.all())
                if iva_ret_rate > 0:
                    r.amount = (iva_total * iva_ret_rate / Decimal("100")).quantize(money)
                elif getattr(profile, "afip_category", "") == "RI":
                    r.amount = (iva_total * Decimal("0.50")).quantize(money)
                else:
                    r.amount = Decimal("0")

            elif r.retention_type == "SUSS":
                suss_rate = Decimal(str(getattr(profile, "suss_retention_rate", 0) or "0"))
                if suss_rate > 0:
                    r.amount = (self.net_amount * suss_rate / Decimal("100")).quantize(money)
                else:
                    r.amount = Decimal("0")

            r.save()

        # 5) Totales finales
        self.tax_amount = sum(
            (t.amount for t in self.taxes.all()), Decimal("0")
        ).quantize(money)
        self.perception_amount = sum(
            (p.amount for p in self.perceptions.all()), Decimal("0")
        ).quantize(money)
        self.retention_amount = sum(
            (r.amount for r in self.retentions.all()), Decimal("0")
        ).quantize(money)

        self.total_amount = (
            self.net_amount
            + self.tax_amount
            + self.perception_amount
            - self.retention_amount
        ).quantize(money)

        self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            from accounting.services import AccountingService

            AccountingService.post_purchase(self)


class PurchaseLine(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="lines")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1.00"))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_lines")
    expense_account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_lines")

    class Meta:
        ordering = ["id"]

    @property
    def subtotal(self):
        return (self.quantity * self.unit_price).quantize(Decimal("0.01"))

    @property
    def tax_amount(self):
        if not self.tax:
            return Decimal("0.00")
        return (self.subtotal * (self.tax.rate / Decimal("100"))).quantize(Decimal("0.01"))


class PurchaseTax(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="taxes")
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_taxes")
    base_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class PurchasePerception(models.Model):
    PERCEPTION_CHOICES = (
        ("IIBB", "Ingresos Brutos"),
        ("IVA", "IVA"),
        ("MUNI", "Municipal"),
        ("INTERNOS", "Impuestos Internos"),
    )
    JURISDICTION_CHOICES = (
        ("ARBA", "Buenos Aires (ARBA)"),
        ("AGIP", "CABA (AGIP)"),
        ("CÓRDOBA", "Córdoba"),
        ("SANTA_FE", "Santa Fe"),
        ("MENDOZA", "Mendoza"),
        ("TUCUMÁN", "Tucumán"),
        ("OTRA", "Otra Jurisdicción"),
    )

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="perceptions")
    perception_type = models.CharField(max_length=10, choices=PERCEPTION_CHOICES)
    jurisdiction = models.CharField(max_length=50, choices=JURISDICTION_CHOICES, default="ARBA", blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class PurchaseRetention(models.Model):
    RETENTION_CHOICES = (
        ("GAN", "Ganancias"),
        ("IVA", "IVA"),
        ("SUSS", "SUSS"),
        ("IIBB", "IIBB"),
    )
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="retentions")
    retention_type = models.CharField(max_length=10, choices=RETENTION_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

