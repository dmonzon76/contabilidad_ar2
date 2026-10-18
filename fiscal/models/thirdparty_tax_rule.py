# fiscal/models/thirdparty_tax_rule.py

from django.core.exceptions import ValidationError
from django.db import models


class ThirdPartyTaxRule(models.Model):

    tax_profile = models.ForeignKey(
        "fiscal.ThirdPartyTaxProfile",
        on_delete=models.CASCADE,
        related_name="rules",
    )

    regime = models.ForeignKey(
        "fiscal.TaxRegime",
        on_delete=models.CASCADE,
        related_name="third_party_rules",
    )

    custom_rate = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = [
            "tax_profile",
            "regime",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "tax_profile",
                    "regime",
                ],
                name="uniq_profile_regime",
            ),
        ]

    def effective_rate(self):
        return self.custom_rate or self.regime.rate

    def clean(self):

        super().clean()

        if (
            self.custom_rate is not None
            and self.custom_rate < 0
        ):
            raise ValidationError(
                {
                    "custom_rate":
                    "Rate cannot be negative."
                }
            )

    def __str__(self):
        return (
            f"{self.tax_profile} - "
            f"{self.regime}"
        )