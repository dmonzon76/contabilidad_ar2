from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone

from purchases.models.purchase import Purchase
from purchases.models.purchase import PurchaseLine
from inventory.models import InventoryMovement
from accounting.models.account_movement import AccountMovement


def purchases_dashboard(request):
    company_id = request.session.get("active_company_id")
    today = timezone.now().date()

    # ============================
    # COMPRAS DEL DÍA
    # ============================
    purchases_today = Purchase.objects.filter(company_id=company_id, date=today)

    purchases_today_total = (
        purchases_today.aggregate(total=Sum("total_amount"))["total"] or 0
    )
    purchases_today_count = purchases_today.count()

    # ============================
    # IVA CRÉDITO DEL DÍA
    # ============================
    iva_credit_today = purchases_today.aggregate(total=Sum("vat_amount"))["total"] or 0

    # ============================
    # ENTRADAS DE INVENTARIO DEL DÍA
    # ============================
    inventory_in_today = (
        InventoryMovement.objects.filter(
            company_id=company_id, movement_type="IN", date=today
        ).aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    # ============================
    # TOP PROVEEDORES DEL DÍA
    # ============================
    top_suppliers_today = (
        purchases_today.values("supplier__name")
        .annotate(total=Sum("total_amount"))
        .order_by("-total")[:10]
    )

    # ============================
    # TOP PRODUCTOS COMPRADOS
    # ============================
    top_products_today = (
        PurchaseLine.objects.filter(
            purchase__company_id=company_id, purchase__date=today
        )
        .values("product__name")
        .annotate(total_qty=Sum("quantity"))
        .order_by("-total_qty")[:10]
    )

    # ============================
    # COMPRAS POR CATEGORÍA
    # ============================
    purchases_by_category_today = (
        PurchaseLine.objects.filter(
            purchase__company_id=company_id, purchase__date=today
        )
        .values("product__category__name")
        .annotate(total=Sum("subtotal"))
        .order_by("-total")
    )

    # ============================
    # COMPRAS POR HORA
    # ============================
    purchases_by_hour_today = (
        purchases_today.values("created_at__hour")
        .annotate(total=Sum("total_amount"))
        .order_by("created_at__hour")
    )

    # ============================
    # CUENTA CORRIENTE PROVEEDORES (DÍA)
    # ============================
    cc_suppliers_today_total = (
        AccountMovement.objects.filter(
            company_id=company_id, supplier__isnull=False, date=today
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    context = {
        "purchases_today_total": purchases_today_total,
        "purchases_today_count": purchases_today_count,
        "iva_credit_today": iva_credit_today,
        "inventory_in_today": inventory_in_today,
        "top_suppliers_today": top_suppliers_today,
        "top_products_today": top_products_today,
        "purchases_by_category_today": purchases_by_category_today,
        "purchases_by_hour_today": purchases_by_hour_today,
        "cc_suppliers_today_total": cc_suppliers_today_total,
    }

    return render(request, "reports/purchases_dashboard.html", context)
