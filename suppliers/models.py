from django.db import models

from company.models import Company
from fiscal.models import ThirdPartyTaxProfile


class Supplier(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="suppliers",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=150)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    tax_profile = models.OneToOneField(
        ThirdPartyTaxProfile,
        on_delete=models.CASCADE,
        related_name="supplier",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
