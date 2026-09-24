from decimal import Decimal
from django.db import models
from company.models import Company
from suppliers.models import Supplier
from accounting.models import Account
from fiscal.models import Tax


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
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    perception_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    retention_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.invoice_number} - {self.supplier.name}"

    def calculate_totals(self):
        money = Decimal("0.01")

        # 1) Subtotal Neto por líneas
        net_total = sum((line.subtotal for line in self.lines.all()), Decimal("0.00"))
        self.net_amount = net_total.quantize(money)

        # 2) Sincronización de IVA por alícuota en PurchaseTax
        tax_by_type = {}
        for line in self.lines.all():
            line_subtotal = line.subtotal
            if line.tax:
                tax_obj = line.tax
                line_vat = line.tax_amount
                if tax_obj not in tax_by_type:
                    tax_by_type[tax_obj] = {"base": Decimal("0.00"), "amount": Decimal("0.00")}
                tax_by_type[tax_obj]["base"] += line_subtotal
                tax_by_type[tax_obj]["amount"] += line_vat

        if self.lines.exists() and tax_by_type:
            self.taxes.exclude(tax__in=tax_by_type.keys()).delete()
            for tax_obj, data in tax_by_type.items():
                p_tax, _ = self.taxes.get_or_create(
                    tax=tax_obj,
                    defaults={
                        "base_amount": data["base"].quantize(money),
                        "amount": data["amount"].quantize(money),
                    },
                )
                p_tax.base_amount = data["base"].quantize(money)
                p_tax.amount = data["amount"].quantize(money)
                p_tax.save(update_fields=["base_amount", "amount"])

        self.tax_amount = sum((t.amount for t in self.taxes.all()), Decimal("0.00")).quantize(money)

        # 3) Percepciones sufridas (IIBB por Jurisdicción, IVA, MUNI, etc.)
        profile = getattr(self.supplier, "tax_profile", None)

        for p in self.perceptions.all():
            if not profile:
                continue

            if p.amount == Decimal("0.00"):
                if p.perception_type == "IIBB":
                    iibb_rate = Decimal(str(getattr(profile, "iibb_percentage", 0) or "0"))
                    if iibb_rate > 0 and getattr(profile, "iibb_status", "") != "EXENTO":
                        p.amount = (self.net_amount * iibb_rate / Decimal("100")).quantize(money)

                elif p.perception_type == "IVA":
                    iva_perc_rate = Decimal(str(getattr(profile, "iva_perception_percentage", 0) or "0"))
                    if iva_perc_rate > 0:
                        p.amount = (self.net_amount * iva_perc_rate / Decimal("100")).quantize(money)
                    elif getattr(profile, "afip_category", "") == "RI":
                        p.amount = (self.net_amount * Decimal("0.03")).quantize(money)

            p.save()

        # 4) Retenciones practicadas
        for r in self.retentions.all():
            if not profile:
                continue

            if r.amount == Decimal("0.00"):
                if r.retention_type == "GAN":
                    gan_rate = Decimal(str(getattr(profile, "ganancias_percentage", 0) or "0"))
                    if gan_rate > 0 and getattr(profile, "ganancias_status", "") != "EXENTO":
                        r.amount = (self.net_amount * gan_rate / Decimal("100")).quantize(money)

                elif r.retention_type == "IVA":
                    if getattr(profile, "afip_category", "") == "RI":
                        r.amount = (self.tax_amount * Decimal("0.50")).quantize(money)

            r.save()

        # 5) Totales finales
        self.perception_amount = sum((p.amount for p in self.perceptions.all()), Decimal("0.00")).quantize(money)
        self.retention_amount = sum((r.amount for r in self.retentions.all()), Decimal("0.00")).quantize(money)

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
