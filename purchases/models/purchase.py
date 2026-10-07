from decimal import Decimal

from django.db import models

from accounting.models import Account
from company.models import Company
from fiscal.models import Tax
from suppliers.models import Supplier


class Purchase(models.Model):
    perceptions: models.Manager["PurchasePerception"]
    retentions: models.Manager["PurchaseRetention"]

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

        lines = list(self.lines.select_related("tax"))
        self.net_amount = sum(
            (line.quantity * line.unit_price for line in lines),
            Decimal("0"),
        ).quantize(money)

        line_tax_amount = sum(
            (line.tax_amount for line in lines if line.tax is not None),
            Decimal("0"),
        ).quantize(money)
        tax_lines = list(self.taxes.select_related("tax"))
        if any(line.tax is not None for line in lines):
            self.tax_amount = line_tax_amount
        else:
            for tax_line in tax_lines:
                if tax_line.tax is None:
                    tax_line.amount = Decimal("0")
                else:
                    if tax_line.base_amount <= 0:
                        tax_line.base_amount = self.net_amount
                    tax_line.amount = (tax_line.base_amount * tax_line.tax.rate / Decimal("100")).quantize(money)
                tax_line.save(update_fields=["base_amount", "amount"])
            self.tax_amount = sum(
                (tax_line.amount for tax_line in tax_lines),
                Decimal("0"),
            ).quantize(money)

        # 3) Percepciones automáticas basadas en perfil fiscal del proveedor
        profile = getattr(self.supplier, "tax_profile", None)
        ganancias_rate = Decimal("0")

        if profile:
            # --- IIBB ---
            is_iibb_agent = getattr(profile, "is_iibb_perception_agent", False)
            iibb_rate = Decimal(str(getattr(profile, "iibb_perception_rate", 0) or "0"))

            if (is_iibb_agent or iibb_rate > 0) and not getattr(profile, "is_iibb_exempt", False):
                self.perceptions.get_or_create(
                    perception_type="IIBB",
                    defaults={"amount": Decimal("0")},
                )

            # --- IVA ---
            is_iva_agent = getattr(profile, "is_iva_perception_agent", False)
            iva_rate = Decimal(str(getattr(profile, "iva_perception_rate", 0) or "0"))
            afip_cat = getattr(profile, "afip_category", "")

            if is_iva_agent or iva_rate > 0:
                self.perceptions.get_or_create(
                    perception_type="IVA",
                    defaults={"amount": Decimal("0")},
                )

            ganancias_rate = Decimal(str(getattr(profile, "ganancias_retention_rate", 0) or "0"))
            if (
                ganancias_rate > 0
                or getattr(profile, "is_ganancias_exempt", False)
                or getattr(profile, "ganancias_status", "") != "INSCRIPTO"
            ):
                self.retentions.get_or_create(
                    retention_type="GAN",
                    defaults={"amount": Decimal("0")},
                )

            iva_ret_rate = Decimal(str(getattr(profile, "iva_retention_rate", 0) or "0"))
            if iva_ret_rate > 0 or afip_cat == "RI":
                self.retentions.get_or_create(
                    retention_type="IVA",
                    defaults={"amount": Decimal("0")},
                )

            iibb_ret_rate = Decimal(str(getattr(profile, "iibb_retention_rate", 0) or "0"))
            if iibb_ret_rate > 0:
                self.retentions.get_or_create(
                    retention_type="IIBB",
                    defaults={"amount": Decimal("0")},
                )

            suss_rate = Decimal(str(getattr(profile, "suss_retention_rate", 0) or "0"))
            if suss_rate > 0:
                self.retentions.get_or_create(
                    retention_type="SUSS",
                    defaults={"amount": Decimal("0")},
                )

        for p in self.perceptions.all():
            if not profile:
                continue

            if p.perception_type == "IIBB":
                if getattr(profile, "is_iibb_exempt", False):
                    p.amount = Decimal("0")
                elif iibb_rate > 0:
                    p.amount = (self.net_amount * iibb_rate / Decimal("100")).quantize(money)
            elif p.perception_type == "IVA":
                if iva_rate > 0:
                    p.amount = (self.net_amount * iva_rate / Decimal("100")).quantize(money)
                elif is_iva_agent and afip_cat == "RI":
                    p.amount = (self.net_amount * Decimal("0.03")).quantize(money)
            if p.perception_type in {"IIBB", "IVA"}:
                p.save(update_fields=["amount"])

        for r in self.retentions.all():
            if not profile:
                continue

            if r.retention_type == "GAN":
                if (
                    getattr(profile, "is_ganancias_exempt", False)
                    or getattr(profile, "ganancias_status", "") != "INSCRIPTO"
                ):
                    r.amount = Decimal("0")
                elif ganancias_rate > 0:
                    r.amount = (self.net_amount * ganancias_rate / Decimal("100")).quantize(money)

            elif r.retention_type == "IVA":
                if iva_ret_rate > 0:
                    r.amount = (self.tax_amount * iva_ret_rate / Decimal("100")).quantize(money)
                elif afip_cat == "RI":
                    r.amount = (self.tax_amount * Decimal("0.50")).quantize(money)

            elif r.retention_type == "IIBB":
                if iibb_ret_rate > 0:
                    r.amount = (self.net_amount * iibb_ret_rate / Decimal("100")).quantize(money)

            elif r.retention_type == "SUSS":
                if suss_rate > 0:
                    r.amount = (self.net_amount * suss_rate / Decimal("100")).quantize(money)

            r.save(update_fields=["amount"])

        self.perception_amount = sum((p.amount for p in self.perceptions.all()), Decimal("0")).quantize(money)
        self.retention_amount = sum((r.amount for r in self.retentions.all()), Decimal("0")).quantize(money)

        self.total_amount = (
            self.net_amount + self.tax_amount + self.perception_amount - self.retention_amount
        ).quantize(money)

        self.save()


class PurchaseLine(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="lines")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1.00"))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_lines")
    expense_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_lines"
    )

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
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="taxes",
    )

    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
    )

    taxable_base = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
    )


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
        ("CORDOBA", "Córdoba"),
        ("SANTA_FE", "Santa Fe"),
        ("MENDOZA", "Mendoza"),
        ("TUCUMAN", "Tucumán"),
        ("OTRA", "Otra Jurisdicción"),
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="perceptions",
    )

    perception_type = models.CharField(
        max_length=10,
        choices=PERCEPTION_CHOICES,
    )

    jurisdiction = models.CharField(
        max_length=50,
        choices=JURISDICTION_CHOICES,
        blank=True,
        null=True,
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    notes = models.CharField(
        max_length=200,
        blank=True,
    )

    def __str__(self):
        if self.jurisdiction:
            return f"{self.get_perception_type_display()} {self.get_jurisdiction_display()}"

        return self.get_perception_type_display()


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
