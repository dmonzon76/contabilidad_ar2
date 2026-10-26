from django.core.exceptions import ValidationError
from django.db import models


class PayrollReceiptLine(models.Model):

    receipt = models.ForeignKey(
        "payroll.PayrollReceipt",
        on_delete=models.CASCADE,
        related_name="lines",
    )

    concept = models.ForeignKey(
        "payroll.SalaryConcept",
        on_delete=models.PROTECT,
        related_name="receipt_lines",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
    )

    unit_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:

        ordering = [
            "concept__code",
        ]

    def clean(self):

        super().clean()

        if self.quantity < 0:

            raise ValidationError(
                {
                    "quantity":
                    "Quantity cannot be negative."
                }
            )

        if self.unit_amount < 0:

            raise ValidationError(
                {
                    "unit_amount":
                    "Unit amount cannot be negative."
                }
            )

    def save(self, *args, **kwargs):

        self.amount = (
            self.quantity
            * self.unit_amount
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.receipt}"
            f" - "
            f"{self.concept.code}"
        )