# fiscal/models/tax_jurisdiction.py

from django.db import models


class TaxJurisdiction(models.Model):
    """
    Tax jurisdiction.

    Examples:
        AFIP
        ARBA
        AGIP
        Córdoba
        Mendoza
        SIRCREB
    """

    code = models.CharField(
        max_length=30,
        unique=True,
    )

    name = models.CharField(
        max_length=100,
    )

    is_national = models.BooleanField(
        default=False,
    )

    is_provincial = models.BooleanField(
        default=False,
    )

    is_municipal = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Tax Jurisdiction"
        verbose_name_plural = "Tax Jurisdictions"

    def __str__(self):
        return self.name