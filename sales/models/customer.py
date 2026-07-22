from django.db import models
from company.models import Company
from fiscal.models import ThirdPartyTaxProfile


class Customer(models.Model):
    """
    Customer model for ERP Sales module.
    Includes fiscal profile, contact data, and company association.
    """

    # --- Company association ---
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    # --- Fiscal profile (AFIP / IVA / IIBB / Ganancias) ---
    tax_profile = models.OneToOneField(
        ThirdPartyTaxProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="customer"
    )

    # --- Basic identity ---
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=20, blank=True, null=True)  # CUIT / DNI

    # --- Contact information ---
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    # --- Address ---
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # --- Classification ---
    customer_type = models.CharField(
        max_length=20,
        choices=[
            ("individual", "Individual"),
            ("company", "Company"),
        ],
        default="company",
        blank=True,
        null=True   
    )

    # --- Internal notes ---
    notes = models.TextField(blank=True, null=True)

    # --- Status ---
    is_active = models.BooleanField(default=True)

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.name} ({self.company.legal_name})"
