import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from company.models import Company
from inventory.models import InventoryMovement
from payroll.models import Employee, FamilyMember, PayrollReceipt
from purchases.models.purchase import Purchase
from sales.models.sale import Sale


@login_required
def main_dashboard(request):
    company_id = request.session.get("active_company_id")
    company = get_object_or_404(Company, pk=company_id)

    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    total_sales_month = (
        Sale.objects.filter(company_id=company_id, date__month=current_month, date__year=current_year)
        .aggregate(total=Sum("total_amount"))["total"]
        or 0
    )
    total_purchases_month = (
        Purchase.objects.filter(company_id=company_id, date__month=current_month, date__year=current_year)
        .aggregate(total=Sum("total_amount"))["total"]
        or 0
    )
    cash_flow_month = total_sales_month - total_purchases_month
    inventory_value = (
        InventoryMovement.objects.filter(company_id=company_id)
        .aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    labels = []
    sales_values = []
    purchases_values = []

    for i in range(6):
        month_offset = 5 - i
        month_number = (current_month - month_offset - 1) % 12 + 1
        year_number = current_year if current_month - month_offset > 0 else current_year - 1

        labels.append(f"{month_number}/{year_number}")

        sales_values.append(
            float(
                Sale.objects.filter(company_id=company_id, date__month=month_number, date__year=year_number)
                .aggregate(total=Sum("total_amount"))["total"]
                or 0
            )
        )
        purchases_values.append(
            float(
                Purchase.objects.filter(company_id=company_id, date__month=month_number, date__year=year_number)
                .aggregate(total=Sum("total_amount"))["total"]
                or 0
            )
        )

    cash_flow_values = [float(sale - purchase) for sale, purchase in zip(sales_values, purchases_values)]

    dashboard_data = {
        "salesPurchases": {
            "labels": labels,
            "sales": sales_values,
            "purchases": purchases_values,
        },
        "cashFlow": {
            "labels": labels,
            "values": cash_flow_values,
        },
    }

    active_employees = Employee.objects.filter(is_active=True).count()
    family_members = FamilyMember.objects.count()
    payroll_receipts = PayrollReceipt.objects.count()
    payroll_cost = PayrollReceipt.objects.aggregate(total=Sum("net_amount"))["total"] or 0

    context = {
        "active_company": company,
        "company": company,
        "today": today,
        "kpi": {
            "total_sales_month": float(total_sales_month),
            "total_purchases_month": float(total_purchases_month),
            "cash_flow_month": float(cash_flow_month),
            "inventory_value": float(inventory_value),
        },
        "active_employees": active_employees,
        "family_members": family_members,
        "payroll_receipts": payroll_receipts,
        "payroll_cost": float(payroll_cost),
        "top_products": [],
        "top_customers": [],
        "alerts": [],
        "dashboard_data_json": json.dumps(dashboard_data),
    }

    return render(request, "dashboard/main_dashboard.html", context)
