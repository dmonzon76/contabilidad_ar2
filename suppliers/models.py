from django.db import models
from django.utils import timezone
from company.models import Company

IVA_CONDITIONS = [
    ("RI", "Responsable Inscripto"),
    ("MONO", "Monotributo"),
    ("EX", "Exento"),
    ("NR", "No Responsable"),
]


class ThirdPartyTaxProfile(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="supplier_tax_profiles",
    )
    name = models.CharField(max_length=150)
    tax_id = models.CharField(max_length=20, blank=True, null=True)
    iva_condition = models.CharField(
        max_length=10,
        choices=IVA_CONDITIONS,
        default="RI",
    )
    iibb_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_iibb_exempt = models.BooleanField(default=False)
    ganancias_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_ganancias_exempt = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.tax_id})" if self.tax_id else self.name


class Supplier(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="suppliers",
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    tax_id = models.CharField(max_length=20, blank=True, null=True)
    iva_condition = models.CharField(
        max_length=10,
        choices=IVA_CONDITIONS,
        default="RI",
    )

    iibb_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_iibb_exempt = models.BooleanField(default=False)

    ganancias_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_ganancias_exempt = models.BooleanField(default=False)

    tax_profile = models.ForeignKey(
        ThirdPartyTaxProfile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("company", "name")

    def __str__(self):
        return f"{self.name} ({self.tax_id})" if self.tax_id else self.name
