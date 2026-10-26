from django.core.exceptions import ValidationError
from django.db import models


class EmployeePosition(models.Model):

    employee = models.ForeignKey(
        "payroll.Employee",
        on_delete=models.CASCADE,
        related_name="positions",
    )

    agreement = models.ForeignKey(
        "payroll.LaborAgreement",
        on_delete=models.PROTECT,
        related_name="employee_positions",
    )

    category = models.ForeignKey(
        "payroll.JobCategory",
        on_delete=models.PROTECT,
        related_name="employee_positions",
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    basic_salary = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    weekly_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=48,
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
            "-start_date",
        ]

    def clean(self):

        super().clean()

        if (
            self.category
            and self.agreement
            and self.category.agreement_id
            != self.agreement_id
        ):
            raise ValidationError(
                {
                    "category":
                    "Category does not belong to selected agreement."
                }
            )

        if (
            self.end_date
            and self.end_date < self.start_date
        ):
            raise ValidationError(
                {
                    "end_date":
                    "End date cannot be before start date."
                }
            )

    def __str__(self):

        return (
            f"{self.employee}"
            f" - "
            f"{self.category}"
        )