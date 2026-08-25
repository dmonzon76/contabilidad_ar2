import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from company.models import Company
from sales.models.sale import Sale
from purchases.models.purchase import Purchase
from inventory.models import InventoryMovement


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
    total_sales_month = (
        Sale.objects.filter(company_id=company_id, date__month=month, date__year=year)
        .aggregate(total=Sum("total_amount"))["total"] or 0
    )

    # -----------------------------
    # KPI — Purchases (Month)
    # -----------------------------
    total_purchases_month = (
        Purchase.objects.filter(company_id=company_id, date__month=month, date__year=year)
        .aggregate(total=Sum("total_amount"))["total"] or 0
    )

    # -----------------------------
    # KPI — Cash Flow (Month)
    # -----------------------------
    cash_flow_month = total_sales_month - total_purchases_month

    # -----------------------------
    # KPI — Inventory Value
    # -----------------------------
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
            float(
                Sale.objects.filter(company_id=company_id, date__month=month_i, date__year=year_i)
                .aggregate(total=Sum("total_amount"))["total"] or 0
            )
        )

        purchases_values.append(
            float(
                Purchase.objects.filter(company_id=company_id, date__month=month_i, date__year=year_i)
                .aggregate(total=Sum("total_amount"))["total"] or 0
            )
        )

    labels.reverse()
    sales_values.reverse()
    purchases_values.reverse()

    # -----------------------------
    # CHART — Cash Flow (Last 6 months)
    # -----------------------------
    cash_flow_values = [float(s - p) for s, p in zip(sales_values, purchases_values)]

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

    context = {
        "active_company": company,
        "company": company,

        "kpi": {
            "total_sales_month": float(total_sales_month),
            "total_purchases_month": float(total_purchases_month),
            "cash_flow_month": float(cash_flow_month),
            "inventory_value": float(inventory_value),
        },

        "top_products": [],
        "top_customers": [],
        "alerts": [],

        "dashboard_data_json": json.dumps(dashboard_data),
    }

    return render(request, "dashboard/main_dashboard.html", context)
