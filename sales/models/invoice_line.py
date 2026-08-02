from django.db import models
from sales.models.invoice import Invoice
from products.models import Product  # ✔ CORRECTO


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="lines"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2)  # 21, 10.5, 27, 0

    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} ({self.quantity} × {self.unit_price})"
