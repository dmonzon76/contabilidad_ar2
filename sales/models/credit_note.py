from django.db import models
from django.utils import timezone

from company.models import Company
from customers.models import Customer
from sales.models.sale import Sale


class CreditNote(models.Model):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("ISSUED", "Issued"),
        ("CANCELLED", "Cancelled"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="credit_notes",
    )

    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name="credit_notes",
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="credit_notes",
    )

    date = models.DateField(
        default=timezone.now,
    )

    number = models.CharField(
        max_length=20,
        blank=True,
    )

    reason = models.TextField()

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-date", "-id"]

        constraints = [
            models.UniqueConstraint(
                fields=["sale"],
                name="unique_credit_note_per_sale",
            )
        ]

    def __str__(self):
        return f"CN {self.number} - Sale {self.sale.number}"

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        if is_new and not self.number:
            last = CreditNote.objects.filter(company=self.company).order_by("-id").first()

            if last and last.number and last.number.isdigit():
                next_number = int(last.number) + 1
            else:
                next_number = 1

            self.number = str(next_number).zfill(6)

        super().save(*args, **kwargs)
