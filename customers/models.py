from django.db import models

from company.models import Company
from fiscal.models import ThirdPartyTaxProfile


class Customer(models.Model):
    """
    Cliente.

    Toda la información fiscal vive en ThirdPartyTaxProfile.
    Este modelo solamente mantiene información comercial.
    """
    tax_profile = models.ForeignKey(
    ThirdPartyTaxProfile,
    on_delete=models.PROTECT,
    related_name="customers",
    null=True,
    blank=True,
)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="customers",
    )

    name = models.CharField(
        max_length=255,
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

    tax_profile = models.ForeignKey(
        ThirdPartyTaxProfile,
        on_delete=models.PROTECT,
        related_name="customers",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("company", "name")

    def __str__(self):
        return self.name