from decimal import Decimal

from django.db import transaction

from payroll.models import (
    Employee,
    PayrollPeriod,
    PayrollReceipt,
    PayrollReceiptLine,
    SalaryConcept,
)


class PayrollCalculator:

    RETIREMENT_RATE = Decimal("0.11")
    INSSJP_RATE = Decimal("0.03")
    HEALTH_INSURANCE_RATE = Decimal("0.03")

    @classmethod
    @transaction.atomic
    def calculate_employee(
        cls,
        employee: Employee,
        period: PayrollPeriod,
    ) -> PayrollReceipt:

        receipt, _ = PayrollReceipt.objects.get_or_create(
            employee=employee,
            period=period,
            defaults={
                "liquidation_date": period.liquidation_date,
            },
        )

        receipt.lines.all().delete()

        position = (
            employee.positions
            .filter(is_active=True)
            .order_by("-start_date")
            .first()
        )

        if not position:
            raise ValueError(
                f"Employee '{employee}' has no active position."
            )

        gross_salary = position.basic_salary

        cls._create_basic_salary_line(
            receipt,
            gross_salary,
        )

        cls._create_retirement_line(
            receipt,
            gross_salary,
        )

        cls._create_inssjp_line(
            receipt,
            gross_salary,
        )

        cls._create_health_insurance_line(
            receipt,
            gross_salary,
        )

        cls._calculate_totals(
            receipt,
        )

        receipt.status = "CALCULATED"
        receipt.save()

        return receipt

    @staticmethod
    def _get_concept(
        code: str,
    ):

        return SalaryConcept.objects.filter(
            code=code,
            is_active=True,
        ).first()

    @classmethod
    def _create_basic_salary_line(
        cls,
        receipt,
        gross_salary,
    ):

        concept = cls._get_concept("001")

        if not concept:
            raise ValueError(
                "Salary concept 001 - Basic Salary not found."
            )

        PayrollReceiptLine.objects.create(
            receipt=receipt,
            concept=concept,
            quantity=1,
            unit_amount=gross_salary,
        )

    @classmethod
    def _create_retirement_line(
        cls,
        receipt,
        gross_salary,
    ):

        concept = cls._get_concept("101")

        if not concept:
            return

        PayrollReceiptLine.objects.create(
            receipt=receipt,
            concept=concept,
            quantity=1,
            unit_amount=(
                gross_salary
                * cls.RETIREMENT_RATE
            ),
        )

    @classmethod
    def _create_inssjp_line(
        cls,
        receipt,
        gross_salary,
    ):

        concept = cls._get_concept("102")

        if not concept:
            return

        PayrollReceiptLine.objects.create(
            receipt=receipt,
            concept=concept,
            quantity=1,
            unit_amount=(
                gross_salary
                * cls.INSSJP_RATE
            ),
        )

    @classmethod
    def _create_health_insurance_line(
        cls,
        receipt,
        gross_salary,
    ):

        concept = cls._get_concept("103")

        if not concept:
            return

        PayrollReceiptLine.objects.create(
            receipt=receipt,
            concept=concept,
            quantity=1,
            unit_amount=(
                gross_salary
                * cls.HEALTH_INSURANCE_RATE
            ),
        )

    @staticmethod
    def _calculate_totals(
        receipt,
    ):

        earnings = Decimal("0.00")
        deductions = Decimal("0.00")

        for line in receipt.lines.select_related(
            "concept"
        ):

            concept_type = (
                line.concept.concept_type
            )

            if concept_type == "EARNING":

                earnings += line.amount

            elif concept_type in (
                "DEDUCTION",
                "EMPLOYEE_CONTRIBUTION",
            ):

                deductions += line.amount

        receipt.total_earnings = earnings
        receipt.total_deductions = deductions
        receipt.net_amount = (
            earnings - deductions
        )

        receipt.save()
