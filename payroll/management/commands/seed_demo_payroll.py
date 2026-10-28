from datetime import date
from random import choice, randint

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

    help = "Create demo payroll dataset"

    EMPLOYEES = [

        ("Ricardo", "Palmer"),
        ("Esteban", "Carrillo"),
        ("Graciela", "Castellano"),
        ("Juan", "Perez"),
        ("Ana", "Gonzalez"),
        ("Marta", "Lopez"),
        ("Carlos", "Rodriguez"),
        ("Laura", "Fernandez"),
        ("Diego", "Martinez"),
        ("Sofia", "Romero"),
        ("Pablo", "Torres"),
        ("Daniela", "Ruiz"),
        ("Jorge", "Morales"),
        ("Sergio", "Alvarez"),
        ("Adrian", "Molina"),
        ("Natalia", "Herrera"),
        ("Roberto", "Vega"),
        ("Gustavo", "Diaz"),
        ("Patricia", "Silva"),
        ("Marcelo", "Acosta"),
    ]

    def handle(self, *args, **kwargs):

        company = Company.objects.first()

        if not company:

            self.stdout.write(
                self.style.ERROR(
                    "No Company found."
                )
            )
            return

        period, _ = PayrollPeriod.objects.get_or_create(
            company=company,
            year=2026,
            month=10,
            defaults={
                "code": "2026-10",
                "liquidation_date": date(
                    2026,
                    10,
                    31,
                ),
                "status": "OPEN",
            },
        )

        categories = {
            "ADM_A": JobCategory.objects.get(
                code="ADM_A"
            ),
            "ADM_B": JobCategory.objects.get(
                code="ADM_B"
            ),
            "SUP": JobCategory.objects.get(
                code="SUP"
            ),
        }

        category_distribution = [

            categories["ADM_A"],
            categories["ADM_A"],
            categories["ADM_A"],
            categories["ADM_A"],
            categories["ADM_A"],

            categories["ADM_B"],
            categories["ADM_B"],
            categories["ADM_B"],
            categories["ADM_B"],
            categories["ADM_B"],
            categories["ADM_B"],
            categories["ADM_B"],

            categories["SUP"],
            categories["SUP"],
            categories["SUP"],
            categories["SUP"],
            categories["SUP"],

            categories["ADM_A"],
            categories["ADM_B"],
            categories["SUP"],
        ]

        created_count = 0

        for idx, (
            first_name,
            last_name,
        ) in enumerate(
            self.EMPLOYEES,
            start=1,
        ):

            employee, created = (
                Employee.objects.get_or_create(
                    company=company,
                    employee_number=f"EMP{idx:04d}",
                    defaults={
                        "first_name": first_name,
                        "last_name": last_name,
                        "cuil":
                            f"20{idx:09d}",
                        "hire_date": date(
                            randint(
                                2000,
                                2025,
                            ),
                            randint(
                                1,
                                12,
                            ),
                            randint(
                                1,
                                28,
                            ),
                        ),
                        "is_active": True,
                    },
                )
            )

            category = category_distribution[
                idx - 1
            ]

            EmployeePosition.objects.get_or_create(
                employee=employee,
                is_active=True,
                defaults={
                    "agreement":
                        category.agreement,
                    "category":
                        category,
                    "start_date":
                        employee.hire_date,
                    "basic_salary":
                        category.base_salary,
                },
            )

            AttendanceRecord.objects.get_or_create(
                employee=employee,
                payroll_period=period,
                defaults={
                    "normal_hours": 160,
                    "overtime_50_hours":
                        randint(0, 10),
                    "overtime_100_hours":
                        randint(0, 5),
                    "absence_days":
                        choice(
                            [0, 0, 0, 1, 2]
                        ),
                    "worked_days":
                        30,
                    "is_approved":
                        True,
                },
            )

            if created:
                created_count += 1

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Demo payroll dataset created"
            )
        )

        self.stdout.write(
            f"Employees processed: "
            f"{len(self.EMPLOYEES)}"
        )

        self.stdout.write(
            f"New employees: "
            f"{created_count}"
        )

        self.stdout.write(
            f"Period: {period.code}"
        )