from django.db import models
from company.models import Company
# Create your models here.



class ThirdPartyTaxProfile(models.Model):
    AFIP_CATEGORY_CHOICES = [
        ("RI", "Responsable Inscripto"),
        ("MONO", "Monotributo"),
        ("EX", "Exento"),
        ("CF", "Consumidor Final"),
        ("NR", "No Responsable"),
        ("MT", "Monotributo Social"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    afip_category = models.CharField(max_length=10, choices=AFIP_CATEGORY_CHOICES)

    vat_21 = models.BooleanField(default=True)
    vat_105 = models.BooleanField(default=False)
    vat_27 = models.BooleanField(default=False)
    vat_exempt = models.BooleanField(default=False)
    vat_non_taxed = models.BooleanField(default=False)

    iibb_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    iibb_exempt = models.BooleanField(default=False)

    ganancias_agent = models.BooleanField(default=False)

    perceptions_enabled = models.BooleanField(default=False)
    retentions_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.legal_name} – {self.afip_category}"
