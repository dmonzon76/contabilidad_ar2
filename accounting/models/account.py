from django.db import models
from company.models import Company
from django.core.exceptions import ValidationError
from django.db.models import Sum


class Account(models.Model):

    ACCOUNT_TYPES = [
        ("ASSET", "Asset"),
        ("LIABILITY", "Liability"),
        ("EQUITY", "Equity"),
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
    ]

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="accounts"
    )

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("company", "code")
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def balance(self):
        from accounting.models import JournalEntryLine

        total = JournalEntryLine.objects.filter(account=self).aggregate(
            s=Sum("debit") - Sum("credit")
        )["s"]
        return total or 0

        def clean(self):
            parts = self.code.split(".")
            for p in parts:
                if not p.isdigit():
                    raise ValidationError("Each code segment must be numeric.")

            if len(parts) > 1:
                parent_code = ".".join(parts[:-1])
                if not Account.objects.filter(
                    company=self.company, code=parent_code
                ).exists():
                    raise ValidationError(f"Parent code {parent_code} does not exist.")


def total_debit(self, company=None):
    qs = self.journal_lines.all()
    if company:
        qs = qs.filter(entry__company=company)
    return qs.aggregate(total=Sum("debit"))["total"] or 0


def total_credit(self, company=None):
    qs = self.journal_lines.all()
    if company:
        qs = qs.filter(entry__company=company)
    return qs.aggregate(total=Sum("credit"))["total"] or 0


def balance(self, company=None):
    return self.total_debit(company) - self.total_credit(company)
