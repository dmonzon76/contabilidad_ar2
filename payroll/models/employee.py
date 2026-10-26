from django.db import models

from company.models import Company


class Employee(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    employee_number = models.CharField(
        max_length=20,
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    cuil = models.CharField(
        max_length=11,
        unique=True,
    )

    hire_date = models.DateField()

    termination_date = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "last_name",
            "first_name",
        ]

    def __str__(self):

        return (
            f"{self.last_name}, "
            f"{self.first_name}"
        )