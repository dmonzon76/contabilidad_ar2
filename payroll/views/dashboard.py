from django.db.models import Count
from django.db.models import Sum
from django.views.generic import TemplateView

from payroll.models import (
    Employee,
    EmployeePosition,
    FamilyMember,
    PayrollReceipt,
)


class PayrollDashboardView(
    TemplateView,
):

    template_name = (
        "payroll/dashboard.html"
    )

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        employees = (
            Employee.objects.filter(
                is_active=True,
            )
            .count()
        )

        family_members = (
            FamilyMember.objects.count()
        )

        receipts = (
            PayrollReceipt.objects.count()
        )

        payroll_cost = (
            PayrollReceipt.objects.aggregate(
                total=Sum("net_amount")
            )["total"]
            or 0
        )

        total_remunerative = (
            PayrollReceipt.objects.aggregate(
                total=Sum(
                    "total_remunerative"
                )
            )["total"]
            or 0
        )

        total_non_remunerative = (
            PayrollReceipt.objects.aggregate(
                total=Sum(
                    "total_non_remunerative"
                )
            )["total"]
            or 0
        )

        total_deductions = (
            PayrollReceipt.objects.aggregate(
                total=Sum(
                    "total_deductions"
                )
            )["total"]
            or 0
        )

        category_stats = (
            EmployeePosition.objects.filter(
                is_active=True,
            )
            .values(
                "category__name",
            )
            .annotate(
                total=Count("id"),
            )
            .order_by(
                "-total",
            )
        )

        latest_receipts = (
            PayrollReceipt.objects.select_related(
                "employee",
            )
            .order_by(
                "-id",
            )[:10]
        )

        context.update(
            {
                "employees": employees,
                "family_members": family_members,
                "receipts": receipts,
                "payroll_cost": payroll_cost,
                "total_remunerative": total_remunerative,
                "total_non_remunerative": total_non_remunerative,
                "total_deductions": total_deductions,
                "category_stats": category_stats,
                "latest_receipts": latest_receipts,
            }
        )

        return context