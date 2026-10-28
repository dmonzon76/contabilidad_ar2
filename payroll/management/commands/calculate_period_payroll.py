from django.core.management.base import BaseCommand

from payroll.models import (
    Employee,
    PayrollPeriod,
)

from payroll.services.payroll_calculator import (
    PayrollCalculator,
)


class Command(BaseCommand):

    help = "Calculate payroll for all active employees in a period"

    def add_arguments(
        self,
        parser,
    ):

        parser.add_argument(
            "period_code",
            type=str,
            help="Example: 2026-10",
        )

    def handle(
        self,
        *args,
        **options,
    ):

        period_code = options["period_code"]

        try:

            period = PayrollPeriod.objects.get(
                code=period_code,
            )

        except PayrollPeriod.DoesNotExist:

            self.stdout.write(
                self.style.ERROR(
                    f"Payroll period {period_code} not found."
                )
            )

            return

        employees = Employee.objects.filter(
            is_active=True,
        )

        processed = 0
        created = 0
        errors = 0

        self.stdout.write("")
        self.stdout.write(
            f"Calculating payroll for period: {period.code}"
        )
        self.stdout.write("-" * 60)

        for employee in employees:

            try:

                receipt = (
                    PayrollCalculator.calculate_employee(
                        employee=employee,
                        period=period,
                    )
                )

                processed += 1
                created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        (
                            f"[OK] "
                            f"{employee} "
                            f"-> Receipt #{receipt.pk}"
                        )
                    )
                )

            except Exception as exc:

                errors += 1

                self.stdout.write(
                    self.style.WARNING(
                        (
                            f"[SKIPPED] "
                            f"{employee} "
                            f"-> {exc}"
                        )
                    )
                )

        self.stdout.write("")
        self.stdout.write("=" * 60)

        self.stdout.write(
            f"Employees processed: {processed}"
        )

        self.stdout.write(
            f"Receipts created: {created}"
        )

        self.stdout.write(
            f"Errors: {errors}"
        )

        self.stdout.write("=" * 60)