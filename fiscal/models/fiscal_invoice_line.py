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

    def __init__(self, *args, **kwargs):
        legacy_price = kwargs.pop("price", None)
        legacy_vat_rate = kwargs.pop("vat_rate", None)

        if legacy_price is not None and "unit_price" not in kwargs:
            kwargs["unit_price"] = legacy_price

        super().__init__(*args, **kwargs)

        if self.company_id is None and self.invoice_id:
            self.company_id = self.invoice.company_id

        if legacy_vat_rate is not None:
            self._legacy_vat_rate = legacy_vat_rate

    def save(self, *args, **kwargs):
        if self.company_id is None and self.invoice_id:
            self.company_id = self.invoice.company_id

        if self.tax_id is None and hasattr(self, "_legacy_vat_rate"):
            rate = Decimal(str(self._legacy_vat_rate))
            if rate <= 1:
                rate *= 100
            self.tax, _ = Tax.objects.get_or_create(
                code=f"IVA_{rate}",
                defaults={
                    "name": f"IVA {rate}%",
                    "rate": rate,
                    "is_vat": rate > 0,
                    "afip_code": {
                        Decimal("10.5"): 4,
                        Decimal("21"): 5,
                        Decimal("27"): 6,
                    }.get(rate, 0),
                },
            )

        super().save(*args, **kwargs)

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
