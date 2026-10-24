# fiscal/models/tax_registry_import.py

from django.db import models

from company.models import Company


class TaxRegistryImport(models.Model):

    REGISTRY_TYPES = [

        ("ARBA_PERC", "ARBA Perceptions"),
        ("ARBA_RET", "ARBA Retentions"),

        ("AGIP_PERC", "AGIP Perceptions"),
        ("AGIP_RET", "AGIP Retentions"),

        ("SIRCREB", "SIRCREB"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="tax_registry_imports",
    )

    registry_type = models.CharField(
        max_length=30,
        choices=REGISTRY_TYPES,
    )

    period = models.CharField(
        max_length=6,
        help_text="YYYYMM",
    )

    source_filename = models.CharField(
        max_length=255,
    )

    imported_at = models.DateTimeField(
        auto_now_add=True,
    )

    records_count = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:

        ordering = [
            "-period",
            "-imported_at",
        ]

        unique_together = (
            "company",
            "registry_type",
            "period",
        )

    def __str__(self):

        return (
            f"{self.registry_type}"
            f" - {self.period}"
        )