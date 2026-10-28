# payroll/models/attendance_record.py

from django.db import models

class AttendanceRecord(models.Model):

    employee = models.ForeignKey(
        "payroll.Employee",
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    payroll_period = models.ForeignKey(
        "payroll.PayrollPeriod",
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    normal_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    overtime_50_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    overtime_100_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    absence_days = models.PositiveIntegerField(
        default=0,
    )

    worked_days = models.PositiveIntegerField(
        default=30,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    is_approved = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-payroll_period__year",
            "-payroll_period__month",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "employee",
                    "payroll_period",
                ],
                name="uniq_employee_attendance_period",
            ),
        ]

    @property
    def has_attendance_bonus(self):

        return self.absence_days == 0

