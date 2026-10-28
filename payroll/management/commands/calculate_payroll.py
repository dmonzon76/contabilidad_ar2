from django.core.management.base import BaseCommand

from payroll.models import Employee, PayrollPeriod
from payroll.services.payroll_calculator import PayrollCalculator


class Command(BaseCommand):

    help = (
        "Calculate payroll for an employee "
        "and period"
    )

    def add_arguments(
        self,
        parser,
    ):

        parser.add_argument(
            "employee_id",
            type=int,
        )

        parser.add_argument(
            "period_id",
            type=int,
        )

    def handle(
        self,
        *args,
        **options,
    ):

        employee = Employee.objects.get(
            pk=options["employee_id"]
        )

        period = PayrollPeriod.objects.get(
            pk=options["period_id"]
        )

        receipt = (
            PayrollCalculator.calculate_employee(
                employee=employee,
                period=period,
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Payroll calculated successfully. "
                f"Receipt ID: {receipt.pk}"
            )
        )

        self.stdout.write(
            f"Employee: {employee}"
        )

        self.stdout.write(
            f"Period: {period}"
        )

        self.stdout.write(
            f"Total Earnings: "
            f"{receipt.total_earnings}"
        )

        self.stdout.write(
            f"Total Deductions: "
            f"{receipt.total_deductions}"
        )

        self.stdout.write(
            f"Net Amount: "
            f"{receipt.net_amount}"
        )
