from datetime import date

from django.core.management.base import BaseCommand

from company.models import Company

from payroll.models import (
    AttendanceRecord,
    Employee,
    EmployeePosition,
    JobCategory,
    PayrollPeriod,
)


class Command(BaseCommand):

    help = (
        "Create demo employee, position, "
        "period and attendance data"
    )

    def handle(
        self,
        *args,
        **kwargs,
    ):

        company = Company.objects.first()

        if not company:

            self.stdout.write(
                self.style.ERROR(
                    "No Company found."
                )
            )
            return

        category = JobCategory.objects.filter(
            code="ADM_B"
        ).first()

        if not category:

            self.stdout.write(
                self.style.ERROR(
                    "JobCategory ADM_B not found. "
                    "Run seed_payroll first."
                )
            )
            return

        employee, created = (
            Employee.objects.get_or_create(
                company=company,
                employee_number="EMP0001",
                defaults={
                    "first_name": "Juan",
                    "last_name": "Perez",
                    "cuil": "20123456789",
                    "hire_date": date(
                        2016,
                        1,
                        1,
                    ),
                    "is_active": True,
                },
            )
        )

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    (
                        f"Employee created: "
                        f"{employee}"
                    )
                )
            )

        position, _ = (
            EmployeePosition.objects.get_or_create(
                employee=employee,
                is_active=True,
                defaults={
                    "agreement":
                        category.agreement,
                    "category":
                        category,
                    "start_date":
                        date(
                            2026,
                            1,
                            1,
                        ),
                    "basic_salary":
                        category.base_salary,
                },
            )
        )

        period, _ = (
            PayrollPeriod.objects.get_or_create(
                company=company,
                year=2026,
                month=10,
                defaults={
                    "code": "2026-10",
                    "liquidation_date":
                        date(
                            2026,
                            10,
                            31,
                        ),
                    "status": "OPEN",
                },
            )
        )

        attendance, _ = (
            AttendanceRecord.objects.get_or_create(
                employee=employee,
                payroll_period=period,
                defaults={
                    "normal_hours": 160,
                    "overtime_50_hours": 8,
                    "overtime_100_hours": 4,
                    "absence_days": 0,
                    "worked_days": 30,
                    "is_approved": True,
                },
            )
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Demo payroll data created."
            )
        )

        self.stdout.write(
            f"Employee ID: {employee.pk}"
        )

        self.stdout.write(
            f"Period ID: {period.pk}"
        )

        self.stdout.write(
            f"Position ID: {position.pk}"
        )

        self.stdout.write(
            f"Attendance ID: {attendance.pk}"
        )