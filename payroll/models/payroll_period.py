from django.core.validators import RegexValidator
from django.db import models

from company.models import Company


class PayrollPeriod(models.Model):

    STATUS_CHOICES = [

        ("OPEN", "Open"),

        ("CALCULATED", "Calculated"),

        ("CLOSED", "Closed"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="payroll_periods",
    )

    code = models.CharField(
    max_length=7,
    unique=True,
    validators=[
        RegexValidator(
            regex=r"^\d{4}-\d{2}$",
            message="Period must be YYYY-MM.",
        )
    ],
    help_text="YYYY-MM",
)
    

    year = models.PositiveIntegerField()

    month = models.PositiveIntegerField()

    liquidation_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN",
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
            "-year",
            "-month",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "year",
                    "month",
                ],
                name="uniq_payroll_period",
            ),
        ]

    def __str__(self):

        return (
            f"{self.year}"
            f"-"
            f"{str(self.month).zfill(2)}"
        )

def clean(self):

    super().clean()

    if self.month < 1 or self.month > 12:

        from django.core.exceptions import ValidationError

        raise ValidationError(
            {
                "month":
                "Month must be between 1 and 12."
            }
        )        