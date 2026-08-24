import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required

from company.models import Company
from sales.models.sale import Sale
from purchases.models.purchase import Purchase
from inventory.models import InventoryMovement
from accounting.models import JournalEntry
from accounting.models.account_movement import AccountMovement


@login_required
def main_dashboard(request):
    company_id = request.session.get("active_company_id")
    company = get_object_or_404(Company, pk=company_id)

    today = timezone.now().date()
    month = today.month
    year = today.year

    # -----------------------------
    # KPI — Sales (Month)
    # -----------------------------
    sales_month_qs = Sale.objects.filter(company_id=company_id, date__month=month, date__year=year)
    total_sales_month = sales_month_qs.aggregate(total=Sum("total_amount"))["total"] or 0

    # -----------------------------
    # KPI — Purchases (Month)
    # -----------------------------
    purchases_month_qs = Purchase.objects.filter(company_id=company_id, date__month=month, date__year=year)
    total_purchases_month = purchases_month_qs.aggregate(total=Sum("total_amount"))["total"] or 0

    # -----------------------------
    # KPI — Cash Flow (Month)
    # -----------------------------
    cash_flow_month = total_sales_month - total_purchases_month

    # -----------------------------
    # KPI — Inventory Value
    # -----------------------------
   # KPI — Inventory Value (por ahora suma de cantidades)
    inventory_value = (
        InventoryMovement.objects.filter(company_id=company_id)
        .aggregate(total=Sum("quantity"))["total"] or 0
)



   # -----------------------------
    # CHART — Sales vs Purchases (Last 6 months)
    # -----------------------------
    labels = []
    sales_values = []
    purchases_values = []

    for i in range(6):
        month_i = (today.month - i - 1) % 12 + 1
        year_i = today.year if today.month - i > 0 else today.year - 1

        labels.append(f"{month_i}/{year_i}")

        sales_values.append(
            Sale.objects.filter(company_id=company_id, date__month=month_i, date__year=year_i)
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

        purchases_values.append(
            Purchase.objects.filter(company_id=company_id, date__month=month_i, date__year=year_i)
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

    labels.reverse()
    sales_values.reverse()
    purchases_values.reverse()

    # -----------------------------
    # CHART — Cash Flow (Last 6 months)
    # -----------------------------
    cash_flow_values = [s - p for s, p in zip(sales_values, purchases_values)]

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

    # -----------------------------
    # TOP PRODUCTS (dummy for now)
    # -----------------------------
    top_products = []

    # -----------------------------
    # TOP CUSTOMERS (dummy for now)
    # -----------------------------
    top_customers = []

    # -----------------------------
    # ALERTS (dummy for now)
    # -----------------------------
    alerts = []

    context = {
        "company": company,
        "today": today,

        "kpi": {
            "total_sales_month": total_sales_month,
            "total_purchases_month": total_purchases_month,
            "cash_flow_month": cash_flow_month,
            "inventory_value": inventory_value,
        },

        "top_products": top_products,
        "top_customers": top_customers,
        "alerts": alerts,

        "dashboard_data_json": json.dumps(dashboard_data),
    }

    return render(request, "dashboard/main_dashboard.html", context)
