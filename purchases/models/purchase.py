from decimal import Decimal

from django.db import models

from company.models import Company
from suppliers.models import Supplier
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
    is_active = models.BooleanField(default=True)

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

        # 3) Percepciones automáticas basadas en el perfil fiscal del supplier
        supplier = self.supplier
        profile = supplier.tax_profile if hasattr(supplier, "tax_profile") else None

        for p in self.perceptions.all():
            if not profile:
                continue

            if p.perception_type == "IIBB":
                if profile.iibb_status == "INSCRIPTO" and profile.iibb_percentage:
                    p.amount = self.net_amount * (
                        profile.iibb_percentage / Decimal("100")
                    )
                else:
                    p.amount = Decimal("0")

            elif p.perception_type == "IVA":
                if (
                    profile.afip_category in {"RI", "MONO"}
                    and not profile.vat_exempt
                    and profile.iva_perception_percentage
                ):
                    p.amount = self.net_amount * (
                        profile.iva_perception_percentage / Decimal("100")
                    )
                else:
                    p.amount = Decimal("0")

            elif p.perception_type == "MUNI":
                p.amount = Decimal("0")

            p.save()

        # 4) Retenciones automáticas basadas en el perfil fiscal del supplier
        for r in self.retentions.all():
            if not profile:
                continue

            if r.retention_type == "GAN":
                if (
                    profile.ganancias_status == "INSCRIPTO"
                    and profile.ganancias_percentage
                ):
                    r.amount = self.net_amount * (
                        profile.ganancias_percentage / Decimal("100")
                    )
                else:
                    r.amount = Decimal("0")

            elif r.retention_type == "IVA":
                iva_total = sum(t.amount for t in self.taxes.all())
                r.amount = (
                    iva_total * Decimal("0.50")
                    if profile.afip_category == "RI"
                    else Decimal("0")
                )

            elif r.retention_type == "SUSS":
                r.amount = (
                    self.net_amount * (profile.suss_percentage / Decimal("100"))
                    if profile.uses_retentions and profile.suss_percentage
                    else Decimal("0")
                )

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
