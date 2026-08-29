from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from fiscal.models.tax import Tax


class FiscalInvoiceLine(models.Model):
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)

    # REFERENCIA STRING → evita circular import
    invoice = models.ForeignKey(
        "fiscal.FiscalInvoice",
        on_delete=models.CASCADE,
        related_name="lines",
    )

    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    tax = models.ForeignKey(Tax, on_delete=models.PROTECT)

    class Meta:
        ordering = ["invoice_id", "id"]

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.unit_price})"

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    @property
    def tax_amount(self):
        return self.line_total * (self.tax.rate / Decimal("100"))

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero")

        if self.unit_price < 0:
            raise ValidationError("Unit price cannot be negative")

