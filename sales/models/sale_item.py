from decimal import Decimal
from django.db import models
from .sale import Sale
from products.models import Product
from fiscal.models.tax import Tax


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items",
        null=True,
        blank=True,
    )

    description = models.CharField(max_length=200)

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Costo para CMV
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost_subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Impuesto asociado (IVA, exento, no gravado, percepción, interno, etc.)
    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sale_items",
    )

    def save(self, *args, **kwargs):
        # Subtotal comercial
        self.subtotal = self.quantity * self.unit_price

        # Costo desde inventario
        if self.product:
            try:
                cost = self.product.get_current_cost()
            except AttributeError:
                cost = Decimal("0.00")

            self.unit_cost = cost
            self.cost_subtotal = self.quantity * self.unit_cost

        super().save(*args, **kwargs)

    @property
    def tax_amount(self):
        """
        Calcula el impuesto del ítem usando Tax.rate
        """
        if not self.tax:
            return Decimal("0.00")

        return self.subtotal * (self.tax.rate / Decimal("100"))

    def __str__(self):
        return f"{self.description} ({self.quantity} × {self.unit_price})"
