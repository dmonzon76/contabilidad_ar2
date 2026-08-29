from decimal import Decimal
from django.db import models

from company.models import Company
from suppliers.models import Supplier
from accounting.models import Account
from fiscal.models.tax import Tax

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

    # ----------------------------------------------------
    # Cálculo automático de totales e impuestos
    # ----------------------------------------------------
    def calculate_totals(self):
        # 1) Subtotales de líneas
        self.net_amount = sum(
            (line.quantity * line.unit_price) for line in self.lines.all()
        )

        # 2) IVA / Impuestos automáticos desde Tax
        for tax_line in self.taxes.all():
            tax_obj = tax_line.tax  # FK a fiscal.models.tax.Tax

            # rate = porcentaje (ej: 21.00)
            # amount = base * (rate / 100)
            tax_line.amount = tax_line.base_amount * (tax_obj.rate / Decimal("100"))
            tax_line.save()

        # 3) Percepciones automáticas basadas en perfil fiscal del supplier
        profile = self.supplier.tax_profile

        for p in self.perceptions.all():
            if not profile:
                p.amount = Decimal("0")
                p.save()
                continue

            # IIBB
            if p.perception_type == "IIBB":
                if profile.iibb_rate and not profile.is_iibb_exempt:
                    p.amount = self.net_amount * (profile.iibb_rate / Decimal("100"))
                else:
                    p.amount = Decimal("0")

            # IVA percepción
            elif p.perception_type == "IVA":
                if profile.iva_condition == "RI":
                    # Si querés, esto también puede venir de Tax
                    p.amount = self.net_amount * Decimal("0.03")
                else:
                    p.amount = Decimal("0")

            # Municipal
            elif p.perception_type == "MUNI":
                p.amount = Decimal("0")

            p.save()

        # 4) Retenciones automáticas basadas en perfil fiscal del supplier
        for r in self.retentions.all():
            if not profile:
                r.amount = Decimal("0")
                r.save()
                continue

            # Ganancias
            if r.retention_type == "GAN":
                if profile.ganancias_rate and not profile.is_ganancias_exempt:
                    r.amount = self.net_amount * (
                        profile.ganancias_rate / Decimal("100")
                    )
                else:
                    r.amount = Decimal("0")

            # IVA retención
            elif r.retention_type == "IVA":
                iva_total = sum(t.amount for t in self.taxes.all())
                r.amount = (
                    iva_total * Decimal("0.50")
                    if profile.iva_condition == "RI"
                    else Decimal("0")
                )

            # SUSS
            elif r.retention_type == "SUSS":
                r.amount = Decimal("0")

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


# ============================================================
# LÍNEAS DE COMPRA
# ============================================================

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


# ============================================================
# IMPUESTOS (IVA / Internos / Otros)
# ============================================================


class PurchaseTax(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="taxes",
    )

    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="purchase_taxes",
    )

    base_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.tax.code} - {self.amount}"


# ============================================================
# PERCEPCIONES
# ============================================================

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


# ============================================================
# RETENCIONES
# ============================================================

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
