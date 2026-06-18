from django.db import models
from company.models import Company

class CompanyActivity(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    code = models.CharField(max_length=20)  # Código AFIP
    description = models.CharField(max_length=200, blank=True)

    is_primary = models.BooleanField(default=False)

    jurisdiction = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional: CABA, BsAs, Córdoba, etc."
    )

    def __str__(self):
        return f"{self.code} - {self.company.name}"
