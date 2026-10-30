from decimal import Decimal

from django.db import transaction

from payroll.models import (
    AttendanceRecord,
    Employee,
    PayrollPeriod,
    PayrollReceipt,
    PayrollReceiptLine,
    SalaryConcept,
    SalaryScaleLine,
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

        scale_line = cls._get_salary_scale_line(
            position,
        )

        if not scale_line:

            raise ValueError(
                (
                    f"No salary scale found for "
                    f"category '{position.category}'."
                )
            )

        basic_salary = (
            scale_line.basic_salary
        )

        fixed_amount = (
            scale_line.fixed_amount
        )

        extraordinary_amount = (
            scale_line.extraordinary_amount
        )

        #
        # HABERES
        #

        cls._create_basic_salary_line(
            receipt,
            basic_salary,
        )

        cls._create_fixed_amount_line(
            receipt,
            fixed_amount,
        )

        cls._create_extraordinary_amount_line(
            receipt,
            extraordinary_amount,
        )

        cls._create_seniority_line(
            receipt,
            employee,
            period,
            basic_salary,
        )

        if attendance:

            cls._create_attendance_bonus_line(
                receipt,
                attendance,
                basic_salary,
            )

            cls._create_overtime_50_line(
                receipt,
                attendance,
                basic_salary,
            )

            cls._create_overtime_100_line(
                receipt,
                attendance,
                basic_salary,
            )

        #
        # Totales parciales
        #

        cls._calculate_totals(
            receipt,
        )

        #
        # Base imponible sólo remunerativa
        #

        remunerative_total = (
            cls._get_remunerative_total(
                receipt,
            )
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

        #
        # Recalcular incluyendo descuentos
        #

        cls._calculate_totals(
            receipt,
        )

        receipt.status = "CALCULATED"

        receipt.save()

        return receipt

    @classmethod
    def _get_salary_scale_line(
        cls,
        position,
    ):

        return (
            SalaryScaleLine.objects
            .filter(
                category=position.category,
            )
            .select_related(
                "category",
                "scale",
            )
            .first()
        )

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
        basic_salary,
    ):

        cls._create_line(
            receipt,
            "001",
            basic_salary,
        )

    @classmethod
    def _create_fixed_amount_line(
        cls,
        receipt,
        amount,
    ):

        if amount <= 0:
            return

        cls._create_line(
            receipt,
            "050",
            amount,
        )

    @classmethod
    def _create_extraordinary_amount_line(
        cls,
        receipt,
        amount,
    ):

        if amount <= 0:
            return

        cls._create_line(
            receipt,
            "060",
            amount,
        )

    @classmethod
    def _create_seniority_line(
        cls,
        receipt,
        employee,
        period,
        basic_salary,
    ):

        years = max(
            0,
            period.year - employee.hire_date.year,
        )

        if years <= 0:
            return

        amount = (
            basic_salary
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
        basic_salary,
    ):

        if attendance.absence_days > 0:
            return

        amount = (
            basic_salary
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
        basic_salary,
    ):

        if attendance.overtime_50_hours <= 0:
            return

        hour_value = (
            basic_salary
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
        basic_salary,
    ):

        if attendance.overtime_100_hours <= 0:
            return

        hour_value = (
            basic_salary
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

    @staticmethod
    def _get_remunerative_total(
        receipt,
    ):

        remunerative_codes = {
            "001",
            "002",
            "003",
            "010",
            "011",
        }

        total = Decimal("0.00")

        for line in receipt.lines.select_related(
            "concept"
        ):

            if (
                line.concept.code
                in remunerative_codes
            ):

                total += line.amount

        return total

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