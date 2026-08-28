# fiscal/models/tax.py

from django.db import models
from django.core.exceptions import ValidationError


class Tax(models.Model):
    """
    Tabla centralizada de impuestos AFIP.
    Todas las tasas se parametrizan aquí.
    """

    code = models.CharField(max_length=20, unique=True)  # Ej: IVA_21, IVA_10_5
    name = models.CharField(max_length=100)

    rate = models.DecimalField(max_digits=5, decimal_places=2)  # 21.00

    # Clasificación fiscal AFIP
    is_vat = models.BooleanField(default=False)
    is_exempt = models.BooleanField(default=False)
    is_non_taxed = models.BooleanField(default=False)
    is_perception = models.BooleanField(default=False)
    is_retention = models.BooleanField(default=False)
    is_internal_tax = models.BooleanField(default=False)

    # Código AFIP para WSFE
    afip_code = models.IntegerField(default=0)

    # Cuenta contable asociada
    account_code = models.CharField(max_length=50, null=True, blank=True)

    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.name} ({self.rate}%)"

    def clean(self):
        if self.rate < 0:
            raise ValidationError("Tax rate cannot be negative")

        if self.is_vat and self.rate == 0:
            raise ValidationError("VAT taxes must have a rate > 0")

        if self.is_exempt and self.rate != 0:
            raise ValidationError("Exempt taxes must have rate = 0")

        if self.is_non_taxed and self.rate != 0:
            raise ValidationError("Non-taxed taxes must have rate = 0")
