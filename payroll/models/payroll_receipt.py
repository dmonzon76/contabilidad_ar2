from django.db import models

from payroll.models.employee import Employee
from payroll.models.payroll_period import PayrollPeriod


class PayrollReceipt(models.Model):

    STATUS_CHOICES = [

        ("DRAFT", "Draft"),

        ("CALCULATED", "Calculated"),

        ("APPROVED", "Approved"),

        ("POSTED", "Posted"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="payroll_receipts",
    )

    period = models.ForeignKey(
        PayrollPeriod,
        on_delete=models.PROTECT,
        related_name="payroll_receipts",
    )

    receipt_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    liquidation_date = models.DateField()

    total_earnings = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    total_deductions = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    net_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-period__year",
            "-period__month",
            "employee__last_name",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "employee",
                    "period",
                ],
                name="uniq_employee_period_receipt",
            ),
        ]

    def __str__(self):

        return (
            f"{self.employee}"
            f" - "
            f"{self.period}"
        )