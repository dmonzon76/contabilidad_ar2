# payroll/services/payroll_calculator.py

from decimal import Decimal

from django.db import transaction

from payroll.models import (
    AttendanceRecord,
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

    SENIORITY_RATE_PER_YEAR = Decimal("0.01")

    ATTENDANCE_BONUS_RATE = Decimal("0.0833")

    MONTHLY_HOURS = Decimal("200")

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

        attendance = (
            AttendanceRecord.objects
            .filter(
                employee=employee,
                payroll_period=period,
            )
            .first()
        )

        gross_salary = position.basic_salary

        #
        # HABERES
        #

        cls._create_basic_salary_line(
            receipt,
            gross_salary,
        )

        cls._create_seniority_line(
            receipt,
            employee,
            period,
            gross_salary,
        )

        if attendance:

            cls._create_attendance_bonus_line(
                receipt,
                attendance,
                gross_salary,
            )

            cls._create_overtime_50_line(
                receipt,
                attendance,
                gross_salary,
            )

            cls._create_overtime_100_line(
                receipt,
                attendance,
                gross_salary,
            )

        cls._calculate_totals(
            receipt,
        )

        remunerative_total = (
            receipt.total_earnings
        )

        #
        # DESCUENTOS
        #

        cls._create_retirement_line(
            receipt,
            remunerative_total,
        )

        cls._create_inssjp_line(
            receipt,
            remunerative_total,
        )

        cls._create_health_insurance_line(
            receipt,
            remunerative_total,
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

        return (
            SalaryConcept.objects
            .filter(
                code=code,
                is_active=True,
            )
            .first()
        )

    @classmethod
    def _create_line(
        cls,
        receipt,
        concept_code,
        amount,
    ):

        concept = cls._get_concept(
            concept_code
        )

        if not concept:
            return

        PayrollReceiptLine.objects.create(
            receipt=receipt,
            concept=concept,
            quantity=1,
            unit_amount=amount,
        )

    #
    # HABERES
    #

    @classmethod
    def _create_basic_salary_line(
        cls,
        receipt,
        gross_salary,
    ):

        cls._create_line(
            receipt,
            "001",
            gross_salary,
        )

    @classmethod
    def _create_seniority_line(
        cls,
        receipt,
        employee,
        period,
        gross_salary,
    ):

        years = max(
            0,
            period.year - employee.hire_date.year,
        )

        if years <= 0:
            return

        amount = (
            gross_salary
            * cls.SENIORITY_RATE_PER_YEAR
            * Decimal(str(years))
        )

        cls._create_line(
            receipt,
            "002",
            amount,
        )

    @classmethod
    def _create_attendance_bonus_line(
        cls,
        receipt,
        attendance,
        gross_salary,
    ):

        if attendance.absence_days > 0:
            return

        amount = (
            gross_salary
            * cls.ATTENDANCE_BONUS_RATE
        )

        cls._create_line(
            receipt,
            "003",
            amount,
        )

    @classmethod
    def _create_overtime_50_line(
        cls,
        receipt,
        attendance,
        gross_salary,
    ):

        if attendance.overtime_50_hours <= 0:
            return

        hour_value = (
            gross_salary
            / cls.MONTHLY_HOURS
        )

        amount = (
            attendance.overtime_50_hours
            * hour_value
            * Decimal("1.5")
        )

        cls._create_line(
            receipt,
            "010",
            amount,
        )

    @classmethod
    def _create_overtime_100_line(
        cls,
        receipt,
        attendance,
        gross_salary,
    ):

        if attendance.overtime_100_hours <= 0:
            return

        hour_value = (
            gross_salary
            / cls.MONTHLY_HOURS
        )

        amount = (
            attendance.overtime_100_hours
            * hour_value
            * Decimal("2")
        )

        cls._create_line(
            receipt,
            "011",
            amount,
        )

    #
    # DESCUENTOS
    #

    @classmethod
    def _create_retirement_line(
        cls,
        receipt,
        gross_amount,
    ):

        amount = (
            gross_amount
            * cls.RETIREMENT_RATE
        )

        cls._create_line(
            receipt,
            "101",
            amount,
        )

    @classmethod
    def _create_inssjp_line(
        cls,
        receipt,
        gross_amount,
    ):

        amount = (
            gross_amount
            * cls.INSSJP_RATE
        )

        cls._create_line(
            receipt,
            "102",
            amount,
        )

    @classmethod
    def _create_health_insurance_line(
        cls,
        receipt,
        gross_amount,
    ):

        amount = (
            gross_amount
            * cls.HEALTH_INSURANCE_RATE
        )

        cls._create_line(
            receipt,
            "103",
            amount,
        )

    #
    # TOTALES
    #

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