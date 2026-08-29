from django.db import models
from company.models import Company
from accounting.models import Account
from fiscal.models.tax import Tax


class Product(models.Model):
    PRODUCT_TYPES = (
        ("PRODUCT", "Product"),  # Mercadería con stock
        ("SERVICE", "Service"),  # Servicio sin stock
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)

    description = models.CharField(max_length=300, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)

    type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default="PRODUCT")

    # Cuenta contable de ingresos
    income_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Cuenta contable de ingreso (Ventas de Mercaderías o Servicios)",
    )

    # Impuesto asociado (IVA, exento, no gravado, internos, etc.)
    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products",
        help_text="Impuesto AFIP asociado al producto",
    )

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.sku})"
