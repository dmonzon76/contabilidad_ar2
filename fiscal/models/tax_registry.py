# fiscal/models/tax_registry.py

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

    valid_from = models.DateField(
        null=True,
        blank=True,
    )

    valid_to = models.DateField(
        null=True,
        blank=True,
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

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "registry_type",
                    "period",
                ],
                name="uniq_registry_period",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "registry_type",
                    "period",
                ]
            ),
        ]

    def __str__(self):

        return (
            f"{self.get_registry_type_display()}"
            f" - "
            f"{self.period}"
        )


class TaxRegistryRate(models.Model):

    registry = models.ForeignKey(
        TaxRegistryImport,
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

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:

        indexes = [
            models.Index(
                fields=["cuit"]
            ),
        ]

    @property
    def effective_rate(self):

        return (
            self.perception_rate
            if self.perception_rate is not None
            else self.retention_rate
        )

    def __str__(self):

        return (
            f"{self.cuit}"
            f" - "
            f"{self.taxpayer_name}"
        )