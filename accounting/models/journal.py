from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from company.models import Company
from .account import Account
from .period import Period

User = get_user_model()


class JournalEntry(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="journal_entries",
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        related_name="journal_entries",
    )
    date = models.DateField()
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_entries",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "id"]

    def __str__(self):
        return f"{self.date} - {self.description}"

    # -----------------------------
    # Totals
    # -----------------------------
    @property
    def total_debit(self):
        return sum(line.debit for line in self.lines.all())

    @property
    def total_credit(self):
        return sum(line.credit for line in self.lines.all())

    @property
    def is_balanced(self):
        return self.total_debit == self.total_credit

    # -----------------------------
    # Validation
    # -----------------------------
    def clean(self):
        super().clean()

        # Period restrictions
        if self.period.is_closed:
            raise ValidationError("Cannot add journal entries to a closed period.")

        if self.period.is_locked:
            raise ValidationError("Cannot modify entries in a locked period.")

        # Balanced entry
        if self.total_debit != self.total_credit:
            raise ValidationError("Journal entry is not balanced.")

    # -----------------------------
    # Save with validation
    # -----------------------------
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class JournalEntryLine(models.Model):
    entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name="lines",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="journal_lines",
    )
    description = models.CharField(max_length=255, blank=True)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.account} D:{self.debit} C:{self.credit}"

    # -----------------------------
    # Validation
    # -----------------------------
    def clean(self):
        # Cannot have both debit and credit
        if self.debit and self.credit:
            raise ValidationError("Line cannot have both debit and credit.")

        # Must have either debit or credit
        if self.debit == 0 and self.credit == 0:
            raise ValidationError("Line must have debit or credit.")

        # Optional: require description for income/expense accounts
        if self.account.type in ("INCOME", "EXPENSE") and not self.description:
            raise ValidationError("Income/Expense lines must include a description.")
