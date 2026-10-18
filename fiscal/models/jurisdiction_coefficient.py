# fiscal/models/jurisdiction_coefficient.py

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class JurisdictionCoefficient(models.Model):
    """
    Convenio Multilateral (CM05).

    Distribución de coeficientes por jurisdicción
    para un contribuyente determinado.
    """

    tax_profile = models.ForeignKey(
        "fiscal.ThirdPartyTaxProfile",
        on_delete=models.CASCADE,
        related_name="jurisdiction_coefficients",
    )

    jurisdiction = models.ForeignKey(
        "fiscal.TaxJurisdiction",
        on_delete=models.PROTECT,
        related_name="coefficients",
    )

    fiscal_year = models.PositiveIntegerField()

    coefficient = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        help_text="CM05 coefficient. Example: 0.352100",
    )

    is_active = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-fiscal_year",
            "jurisdiction__name",
        ]

        verbose_name = "Jurisdiction Coefficient"
        verbose_name_plural = "Jurisdiction Coefficients"

        constraints = [
            # Un solo coeficiente por
            # perfil + jurisdicción + año
            models.UniqueConstraint(
                fields=[
                    "tax_profile",
                    "jurisdiction",
                    "fiscal_year",
                ],
                name="uniq_jurisdiction_coefficient",
            ),
            # No negativos
            models.CheckConstraint(
                condition=Q(coefficient__gte=0),
                name="coef_gte_zero",
            ),
            # No mayores a 1
            models.CheckConstraint(
                condition=Q(coefficient__lte=1),
                name="coef_lte_one",
            ),
            # Año razonable
            models.CheckConstraint(
                condition=Q(fiscal_year__gte=2000),
                name="coef_year_gte_2000",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "tax_profile",
                    "fiscal_year",
                ],
                name="idx_cm_profile_year",
            ),
            models.Index(
                fields=[
                    "jurisdiction",
                    "fiscal_year",
                ],
                name="idx_cm_jurisdiction_year",
            ),
        ]

    def __str__(self):
        return f"{self.tax_profile} - {self.jurisdiction} - {self.fiscal_year} - {self.coefficient}"

    def clean(self):

        super().clean()

        if self.coefficient is None:
            raise ValidationError({"coefficient": "Coefficient is required."})

        if self.coefficient < Decimal("0"):
            raise ValidationError({"coefficient": "Coefficient cannot be negative."})

        if self.coefficient > Decimal("1"):
            raise ValidationError({"coefficient": "Coefficient cannot exceed 1.000000."})

        # Sólo aplica a sujetos de Convenio Multilateral

        if self.tax_profile and self.tax_profile.iibb_status != "MULTILATERAL":
            raise ValidationError(
                {
                    "tax_profile": (
                        "Jurisdiction coefficients can only be assigned to taxpayers with Multilateral status."
                    )
                }
            )
