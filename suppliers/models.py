from django.db import models

from company.models import Company
from fiscal.models import ThirdPartyTaxProfile


class Supplier(models.Model):
    """
    Proveedor.

    La información comercial vive aquí.
    La información fiscal vive en ThirdPartyTaxProfile.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="suppliers",
    )

    name = models.CharField(
        max_length=255,
    )

    tax_id = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
        verbose_name="CUIT",
    )

    tax_profile = models.ForeignKey(
        ThirdPartyTaxProfile,
        on_delete=models.PROTECT,
        related_name="suppliers",
        null=True,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("company", "name")

    def __str__(self):
        return f"{self.name}" 