from decimal import Decimal
from django.db import models
from .sale import Sale
from products.models import Product


class SaleItem(models.Model):
    TAX_CHOICES = [
        ("GRAVADO", "Gravado"),
        ("EXENTO", "Exento"),
        ("NO_GRAVADO", "No gravado"),
    ]

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items",
        null=True,
        blank=True
    )

    description = models.CharField(max_length=200)

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Costo para CMV
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost_subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    tax_category = models.CharField(
        max_length=20,
        choices=TAX_CHOICES,
        default="GRAVADO"
    )

    def save(self, *args, **kwargs):
        # Subtotal de venta
        self.subtotal = self.quantity * self.unit_price

        # Costo real desde inventario
        if self.product:
            self.unit_cost = self.product.get_current_cost()
            self.cost_subtotal = self.quantity * self.unit_cost

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} ({self.quantity} × {self.unit_price})"
