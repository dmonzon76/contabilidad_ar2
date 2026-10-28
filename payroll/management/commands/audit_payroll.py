from django.core.management.base import BaseCommand

from payroll.models import (
    AttendanceRecord,
    Employee,
    EmployeePosition,
    JobCategory,
    LaborAgreement,
    PayrollPeriod,
    PayrollReceipt,
    SalaryConcept,
)


class Command(BaseCommand):

    help = "Payroll module audit"

    def handle(
        self,
        *args,
        **options,
    ):

        self.stdout.write("")
        self.stdout.write(
            "=" * 60
        )

        self.stdout.write(
            "PAYROLL MODULE AUDIT"
        )

        self.stdout.write(
            "=" * 60
        )

        self.audit_master_data()

        self.audit_employees()

        self.audit_periods()

        self.audit_receipts()

    def audit_master_data(self):

        self.stdout.write("")
        self.stdout.write(
            "MASTER DATA"
        )

        self.stdout.write(
            "-" * 60
        )

        self.stdout.write(
            f"Employees: "
            f"{Employee.objects.count()}"
        )

        self.stdout.write(
            f"Labor Agreements: "
            f"{LaborAgreement.objects.count()}"
        )

        self.stdout.write(
            f"Categories: "
            f"{JobCategory.objects.count()}"
        )

        self.stdout.write(
            f"Salary Concepts: "
            f"{SalaryConcept.objects.count()}"
        )

        self.stdout.write(
            f"Periods: "
            f"{PayrollPeriod.objects.count()}"
        )

        self.stdout.write(
            f"Positions: "
            f"{EmployeePosition.objects.count()}"
        )

        self.stdout.write(
            f"Attendance Records: "
            f"{AttendanceRecord.objects.count()}"
        )

        self.stdout.write(
            f"Receipts: "
            f"{PayrollReceipt.objects.count()}"
        )

    def audit_employees(self):

        self.stdout.write("")
        self.stdout.write(
            "EMPLOYEE ANALYSIS"
        )

        self.stdout.write(
            "-" * 60
        )

        for employee in Employee.objects.all():

            self.stdout.write("")

            self.stdout.write(
                f"[{employee.pk}] {employee}"
            )

            active_position = (
                employee.positions
                .filter(
                    is_active=True,
                )
                .first()
            )

            if active_position:

                self.stdout.write(
                    f"Position: "
                    f"{active_position.category.name}"
                )

                self.stdout.write(
                    f"Agreement: "
                    f"{active_position.agreement.name}"
                )

                self.stdout.write(
                    f"Basic Salary: "
                    f"{active_position.basic_salary}"
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        "WARNING: Employee without active position."
                    )
                )

            attendance_count = (
                employee.attendance_records.count()
            )

            self.stdout.write(
                f"Attendance Records: "
                f"{attendance_count}"
            )

            receipts_count = (
                employee.payroll_receipts.count()
            )

            self.stdout.write(
                f"Receipts: "
                f"{receipts_count}"
            )

    def audit_periods(self):

        self.stdout.write("")
        self.stdout.write(
            "PAYROLL PERIODS"
        )

        self.stdout.write(
            "-" * 60
        )

        for period in PayrollPeriod.objects.all():

            self.stdout.write("")

            self.stdout.write(
                f"{period.code}"
            )

            self.stdout.write(
                f"Status: "
                f"{period.status}"
            )

            self.stdout.write(
                f"Receipts: "
                f"{period.payroll_receipts.count()}"
            )

            self.stdout.write(
                f"Attendance: "
                f"{period.attendance_records.count()}"
            )

    def audit_receipts(self):

        self.stdout.write("")
        self.stdout.write(
            "PAYROLL RECEIPTS"
        )

        self.stdout.write(
            "-" * 60
        )

        for receipt in PayrollReceipt.objects.select_related(
            "employee",
            "period",
        ):

            self.stdout.write("")

            self.stdout.write(
                f"Receipt #{receipt.pk}"
            )

            self.stdout.write(
                f"Employee: "
                f"{receipt.employee}"
            )

            self.stdout.write(
                f"Period: "
                f"{receipt.period}"
            )

            self.stdout.write(
                f"Earnings: "
                f"{receipt.total_earnings}"
            )

            self.stdout.write(
                f"Deductions: "
                f"{receipt.total_deductions}"
            )

            self.stdout.write(
                f"Net Amount: "
                f"{receipt.net_amount}"
            )

            self.stdout.write(
                f"Status: "
                f"{receipt.status}"
            )