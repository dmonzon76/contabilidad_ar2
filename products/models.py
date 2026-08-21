from django.db import models
from company.models import Company
from accounting.models import Account


class Product(models.Model):
    PRODUCT_TYPES = (
        ("PRODUCT", "Product"),  # Mercadería con stock
        ("SERVICE", "Service"),  # Servicio sin stock
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)

    # Descripción corta
    description = models.CharField(max_length=300, blank=True, null=True)

    # NUEVO: detalle largo del servicio
    detail = models.TextField(blank=True, null=True)

    # Tipo de artículo
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default="PRODUCT")

    # NUEVO: cuenta contable para ventas
    income_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Cuenta contable de ingreso (Ventas de Mercaderías o Servicios)",
    )

    # Precio de venta
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.sku})"
