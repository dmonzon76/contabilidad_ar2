from django.db import models

from company.models import Company


class LaborAgreement(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="labor_agreements",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    union_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "name",
        ]

    def __str__(self):

        return self.name
