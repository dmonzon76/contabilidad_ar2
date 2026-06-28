from django.db import models
from company.models import Company


class CompanyProfile(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    # IVA
    vat_21 = models.BooleanField(default=True)
    vat_105 = models.BooleanField(default=False)
    vat_27 = models.BooleanField(default=False)
    vat_exempt = models.BooleanField(default=False)
    vat_non_taxed = models.BooleanField(default=False)

    # IIBB
    IIBB_STATUS = [
        ("LOCAL", "Local"),
        ("MULTILATERAL", "Multilateral"),
        ("EXEMPT", "Exempt"),
    ]
    iibb_status = models.CharField(max_length=20, choices=IIBB_STATUS, default="LOCAL")

    # Ganancias
    GANANCIAS_STATUS = [
        ("INSCRIPTO", "Inscripto"),
        ("NO_INSCRIPTO", "No Inscripto"),
        ("EXENTO", "Exento"),
    ]
    ganancias_status = models.CharField(max_length=20, choices=GANANCIAS_STATUS, default="INSCRIPTO")

    # Percepciones / Retenciones
    uses_perceptions = models.BooleanField(default=False)
    uses_retentions = models.BooleanField(default=False)

    def __str__(self):
        return f"Tax Profile for {self.company.name}"
