from django.db import models

from company.models import Company


class SalaryConcept(models.Model):

    CONCEPT_TYPES = [

        ("EARNING", "Earning"),
        ("DEDUCTION", "Deduction"),

        ("EMPLOYEE_CONTRIBUTION", "Employee Contribution"),
        ("EMPLOYER_CONTRIBUTION", "Employer Contribution"),

        ("INFORMATIONAL", "Informational"),
    ]

    CALCULATION_TYPES = [

        ("FIXED_AMOUNT", "Fixed Amount"),

        ("PERCENTAGE", "Percentage"),

        ("FORMULA", "Formula"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_concepts",
    )

    code = models.CharField(
        max_length=20,
    )

    name = models.CharField(
        max_length=255,
    )

    concept_type = models.CharField(
        max_length=30,
        choices=CONCEPT_TYPES,
    )

    calculation_type = models.CharField(
        max_length=30,
        choices=CALCULATION_TYPES,
        default="FIXED_AMOUNT",
    )

    default_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    percentage = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )

    formula = models.TextField(
        blank=True,
        null=True,
    )

    is_remunerative = models.BooleanField(
        default=True,
    )

    affects_sac = models.BooleanField(
        default=True,
    )

    affects_vacation = models.BooleanField(
        default=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "code",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "company",
                    "code",
                ],
                name="uniq_salary_concept_code",
            ),
        ]

    def __str__(self):

        return (
            f"{self.code}"
            f" - "
            f"{self.name}"
        )