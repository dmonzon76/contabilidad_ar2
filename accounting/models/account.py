from django.db import models
from company.models import Company


class Account(models.Model):

    ACCOUNT_TYPES = [
        ("ASSET", "Asset"),
        ("LIABILITY", "Liability"),
        ("EQUITY", "Equity"),
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="accounts"
    )

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("company", "code")
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def level(self):
        """Devuelve el nivel jerárquico según la cantidad de puntos en el código."""
        return self.code.count(".")
