# fiscal/models/tax_regime.py

from django.db import models


class TaxRegime(models.Model):

    TAX_TYPE_CHOICES = [
        ("VAT", "VAT"),
        ("PROFIT", "Profit Tax"),
        ("IIBB", "Turnover Tax"),
        ("SUSS", "Social Security"),
        ("OTHER", "Other"),
    ]

    APPLICATION_CHOICES = [
        ("PERCEPTION", "Perception"),
        ("RETENTION", "Retention"),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    name = models.CharField(
        max_length=150,
    )

    tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPE_CHOICES,
    )

    application_type = models.CharField(
        max_length=20,
        choices=APPLICATION_CHOICES,
    )

    tax = models.ForeignKey(
        "fiscal.Tax",
        on_delete=models.PROTECT,
        related_name="regimes",
    )

    jurisdiction = models.ForeignKey(
        "fiscal.TaxJurisdiction",
        on_delete=models.PROTECT,
        related_name="regimes",
        null=True,
        blank=True,
    )

    rate = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
    )

    minimum_base = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    account_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    valid_from = models.DateField(
        null=True,
        blank=True,
    )

    valid_to = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "tax_type",
            "application_type",
            "name",
        ]

    def __str__(self):
        return self.name