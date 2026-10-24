# fiscal/models/tax_registry_rate.py

from django.db import models


class TaxRegistryRate(models.Model):

    registry = models.ForeignKey(
        "fiscal.TaxRegistryImport",
        on_delete=models.CASCADE,
        related_name="rates",
    )

    cuit = models.CharField(
        max_length=11,
        db_index=True,
    )

    taxpayer_name = models.CharField(
        max_length=255,
    )

    perception_rate = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )

    retention_rate = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )

    class Meta:

        indexes = [
            models.Index(fields=["cuit"]),
        ]

    def __str__(self):

        return (
            f"{self.cuit} "
            f"{self.taxpayer_name}"
        )