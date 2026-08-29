from django.db import models
from company.models import Company


class ThirdPartyTaxProfile(models.Model):

    AFIP_CATEGORY_CHOICES = [
        ("RI", "Responsable Inscripto"),
        ("MONO", "Monotributo"),
        ("EX", "Exento"),
        ("CF", "Consumidor Final"),
        ("NR", "No Responsable"),
        ("MT", "Monotributo Social"),
    ]

    GANANCIAS_STATUS_CHOICES = [
        ("INSCRIPTO", "Inscripto"),
        ("EXENTO", "Exento"),
        ("NO_CORRESPONDE", "No corresponde (Monotributista)"),
    ]

    IIBB_STATUS_CHOICES = [
        ("INSCRIPTO", "Inscripto"),
        ("EXENTO", "Exento"),
        ("NO_CORRESPONDE", "No corresponde"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="fiscal_tax_profiles",
    )

    customer = models.OneToOneField(
        "sales.Customer",
        on_delete=models.CASCADE,
        related_name="customer_tax_profile",
        null=True,
        blank=True,
    )

    afip_category = models.CharField(max_length=10, choices=AFIP_CATEGORY_CHOICES)
    vat_21 = models.BooleanField(default=True)
    vat_105 = models.BooleanField(default=False)
    vat_27 = models.BooleanField(default=False)
    vat_exempt = models.BooleanField(default=False)
    vat_non_taxed = models.BooleanField(default=False)

    ganancias_status = models.CharField(
        max_length=20,
        choices=GANANCIAS_STATUS_CHOICES,
        default="NO_CORRESPONDE",
    )

    iibb_status = models.CharField(
        max_length=20,
        choices=IIBB_STATUS_CHOICES,
        default="NO_CORRESPONDE",
    )

    uses_perceptions = models.BooleanField(default=False)
    uses_retentions = models.BooleanField(default=False)

    iibb_percentage = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    iva_perception_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=0,
    )
    ganancias_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=0,
    )
    suss_percentage = models.DecimalField(max_digits=6, decimal_places=4, default=0)

    def __str__(self):
        if self.customer:
            return f"{self.company.name} – Tax Profile for {self.customer.name}"
        return f"{self.company.name} – Tax Profile"
