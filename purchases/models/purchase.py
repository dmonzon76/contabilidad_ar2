from decimal import Decimal

from django.db import models

from company.models import Company
from purchases.models.supplier import Supplier
from accounting.models import Account


class Purchase(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="purchases"
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


    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.invoice_number} - {self.supplier.name}"

    # ----------------------------------------------------
    # Cálculo automático de totales e impuestos
    # ----------------------------------------------------
    def calculate_totals(self):
        # 1) Subtotales de líneas
        self.net_amount = sum(
            (line.quantity * line.unit_price) for line in self.lines.all()
        )

        # 2) IVA automático
        for tax in self.taxes.all():
            if tax.vat_type == "21":
                tax.amount = tax.base_amount * Decimal("0.21")
            elif tax.vat_type == "105":
                tax.amount = tax.base_amount * Decimal("0.105")
            elif tax.vat_type == "27":
                tax.amount = tax.base_amount * Decimal("0.27")
            elif tax.vat_type == "0":
                tax.amount = Decimal("0")
            tax.save()

        # 3) Percepciones automáticas (ejemplo, ajustar a tu ThirdPartyTaxProfile)
        supplier = self.supplier
        profile = supplier.tax_profile if hasattr(supplier, "tax_profile") else None

        for p in self.perceptions.all():
            if not profile:
                # si no hay perfil, no calculamos nada automático
                continue

            if p.perception_type == "IIBB":
                # suponemos profile.iibb_rate en %
                p.amount = self.net_amount * Decimal(str(profile.iibb_rate)) / 100

            elif p.perception_type == "IVA":
                # ejemplo simple: RI 3%, MONO 1%
                if getattr(profile, "iva_condition", None) == "RI":
                    p.amount = self.net_amount * Decimal("0.03")
                elif getattr(profile, "iva_condition", None) == "MONO":
                    p.amount = self.net_amount * Decimal("0.01")
                else:
                    p.amount = Decimal("0")

            elif p.perception_type == "MUNI":
                # suponemos profile.muni_rate en %
                p.amount = self.net_amount * Decimal(str(profile.muni_rate)) / 100

            p.save()

        # 4) Retenciones automáticas (ejemplo, ajustar a tu ThirdPartyTaxProfile)
        for r in self.retentions.all():
            if not profile:
                continue

            if r.retention_type == "GAN":
                # RG 830: si supera mínimo no imponible
                minimo = getattr(profile, "ganancias_minimo_no_imponible", Decimal("0"))
                rate = Decimal(str(getattr(profile, "ganancias_rate", 0)))
                if self.net_amount > minimo:
                    r.amount = self.net_amount * rate / 100
                else:
                    r.amount = Decimal("0")

            elif r.retention_type == "IVA":
                # RG 2854: 50% del IVA facturado
                iva_total = sum(t.amount for t in self.taxes.all())
                r.amount = iva_total * Decimal("0.50")

            elif r.retention_type == "SUSS":
                rate = Decimal(str(getattr(profile, "suss_rate", 0)))
                r.amount = self.net_amount * rate / 100

            r.save()

        # 5) Totales finales
        self.tax_amount = sum(t.amount for t in self.taxes.all())
        self.perception_amount = sum(p.amount for p in self.perceptions.all())
        self.retention_amount = sum(r.amount for r in self.retentions.all())

        self.total_amount = (
            self.net_amount
            + self.tax_amount
            + self.perception_amount
            - self.retention_amount
        )

        self.save()


class PurchaseLine(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="lines",
    )
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expense_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="purchase_lines",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.description} ({self.purchase})"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price


class PurchaseTax(models.Model):
    VAT_CHOICES = (
        ("0", "0%"),
        ("105", "10.5%"),
        ("21", "21%"),
        ("27", "27%"),
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="taxes",
    )
    vat_type = models.CharField(max_length=10, choices=VAT_CHOICES)
    base_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"VAT {self.vat_type} - {self.amount}"


class PurchasePerception(models.Model):
    PERCEPTION_CHOICES = (
        ("IIBB", "IIBB"),
        ("IVA", "IVA"),
        ("MUNI", "Municipal"),
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="perceptions",
    )
    perception_type = models.CharField(max_length=10, choices=PERCEPTION_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.perception_type} - {self.amount}"


class PurchaseRetention(models.Model):
    RETENTION_CHOICES = (
        ("GAN", "Ganancias"),
        ("IVA", "IVA"),
        ("SUSS", "SUSS"),
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="retentions",
    )
    retention_type = models.CharField(max_length=10, choices=RETENTION_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.retention_type} - {self.amount}"
