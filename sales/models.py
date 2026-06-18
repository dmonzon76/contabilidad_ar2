from django.db import models
from company.models import Company
from fiscal.models import ThirdPartyTaxProfile
# Create your models here.



class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    tax_profile = models.OneToOneField(
        ThirdPartyTaxProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.company.legal_name})"
