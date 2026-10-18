# fiscal/models/thirdparty_tax.py

from django.db import models

from company.models import Company


class ThirdPartyTaxProfile(models.Model):

    AFIP_CATEGORY_CHOICES = [
        ("RI", "Responsible Registered"),
        ("MONO", "Monotaxpayer"),
        ("EX", "Exempt"),
        ("CF", "Final Consumer"),
        ("NR", "Non Registered"),
        ("MT", "Social Monotaxpayer"),
    ]

    IIBB_STATUS_CHOICES = [
        ("LOCAL", "Local Taxpayer"),
        ("MULTILATERAL", "Multilateral Agreement"),
        ("EXEMPT", "Exempt"),
        ("NON_REGISTERED", "Non Registered"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="tax_profiles",
    )

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    afip_category = models.CharField(
        max_length=20,
        choices=AFIP_CATEGORY_CHOICES,
        default="RI",
    )

    iibb_status = models.CharField(
        max_length=20,
        choices=IIBB_STATUS_CHOICES,
        default="LOCAL",
    )

    is_active = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )
    multilateral_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    has_multilateral_agreement = models.BooleanField(
        default=False,
    )
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
