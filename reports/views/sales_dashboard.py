from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone

from sales.models.sale import Sale
from sales.models.sale_item import SaleItem
from inventory.models import InventoryMovement
from accounting.models import JournalEntry


def sales_dashboard(request):
    company_id = request.session.get("active_company_id")
    today = timezone.now().date()

    # ============================
    # VENTAS DEL DÍA
    # ============================
    sales_today = Sale.objects.filter(
        company_id=company_id,
        date=today
    )

    sales_today_total = sales_today.aggregate(total=Sum("total_amount"))["total"] or 0
    sales_today_count = sales_today.count()

    # ============================
    # IVA DÉBITO DEL DÍA
    # ============================
    iva_debit_today = sales_today.aggregate(total=Sum("vat_amount"))["total"] or 0

    # ============================
    # CMV DEL DÍA
    # ============================
    cmv_today = sales_today.aggregate(total=Sum("cost_total"))["total"] or 0

    # ============================
    # MARGEN DEL DÍA
    # ============================
    margin_today = sales_today_total - cmv_today

    # ============================
    # TOP PRODUCTOS DEL DÍA
    # ============================
    top_products_today = (
        SaleItem.objects.filter(sale__company_id=company_id, sale__date=today)
        .values("product__name")
        .annotate(total_qty=Sum("quantity"))
        .order_by("-total_qty")[:10]
    )

    # ============================
    # VENTAS POR CATEGORÍA
    # ============================
    sales_by_category_today = (
        SaleItem.objects.filter(sale__company_id=company_id, sale__date=today)
        .values("product__category__name")
        .annotate(total=Sum("subtotal"))
        .order_by("-total")
    )

    # ============================
    # VENTAS POR HORA
    # ============================
    sales_by_hour_today = (
        sales_today
        .values("created_at__hour")
        .annotate(total=Sum("total_amount"))
        .order_by("created_at__hour")
    )

    # ============================
    # TOP CLIENTES DEL DÍA
    # ============================
    top_customers_today = (
        sales_today
        .values("customer__name")
        .annotate(total=Sum("total_amount"))
        .order_by("-total")[:10]
    )

    context = {
        "sales_today_total": sales_today_total,
        "sales_today_count": sales_today_count,
        "iva_debit_today": iva_debit_today,
        "cmv_today": cmv_today,
        "margin_today": margin_today,
        "top_products_today": top_products_today,
        "sales_by_category_today": sales_by_category_today,
        "sales_by_hour_today": sales_by_hour_today,
        "top_customers_today": top_customers_today,
    }

    return render(request, "reports/sales_dashboard.html", context)
