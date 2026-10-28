from django.db import models


class SalaryScaleLine(models.Model):

    scale = models.ForeignKey(
        "payroll.SalaryScale",
        on_delete=models.CASCADE,
        related_name="lines",
    )

    group_name = models.CharField(
        max_length=100,
    )

    category_name = models.CharField(
        max_length=10,
    )

    category = models.ForeignKey(
        "payroll.JobCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="salary_scale_links",
    )

    basic_salary = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    fixed_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    extraordinary_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )