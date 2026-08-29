from decimal import Decimal
from django.db import models

from fiscal.models.tax import Tax

class FiscalProduct(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="fiscal_products",
        help_text="Impuesto fiscal centralizado. Si se deja vacío, se usa vat_rate como compatibilidad.",
    )
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=21)

    @property
    def effective_vat_rate(self):
        return self.tax.rate if self.tax else self.vat_rate

    def __str__(self):
        return self.name
