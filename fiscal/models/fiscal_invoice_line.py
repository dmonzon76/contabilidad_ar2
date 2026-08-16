from django.db import models
from fiscal.models.fiscal_invoice import FiscalInvoice


class FiscalInvoiceLine(models.Model):
    invoice = models.ForeignKey(FiscalInvoice, on_delete=models.CASCADE, related_name="lines")

    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=21)

    def line_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.price})"
