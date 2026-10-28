from django.db import models


class SalaryScale(models.Model):

    agreement = models.ForeignKey(
        "payroll.LaborAgreement",
        on_delete=models.CASCADE,
        related_name="salary_scales",
    )

    period = models.CharField(
        max_length=7,
        help_text="YYYY-MM",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "agreement",
                    "period",
                ],
                name="uniq_salary_scale",
            )
        ]

    def __str__(self):

        return (
            f"{self.agreement}"
            f" - "
            f"{self.period}"
        )