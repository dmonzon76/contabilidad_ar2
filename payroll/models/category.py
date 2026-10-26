from django.db import models


class JobCategory(models.Model):

    agreement = models.ForeignKey(
        "payroll.LaborAgreement",
        on_delete=models.CASCADE,
        related_name="categories",
    )

    code = models.CharField(
        max_length=30,
    )

    name = models.CharField(
        max_length=255,
    )

    base_salary = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:

        ordering = [
            "agreement",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "agreement",
                    "code",
                ],
                name="uniq_category_code_by_agreement",
            ),
        ]

    def __str__(self):

        return (
            f"{self.agreement.name}"
            f" - "
            f"{self.name}"
        )