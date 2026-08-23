from django.shortcuts import render
from django.db.models import Sum, Count, F
from django.utils import timezone

from inventory.models import InventoryItem, InventoryMovement
from purchases.models.purchase_line import PurchaseLine
from sales.models.sale_item import SaleItem


def inventory_dashboard(request):
    company_id = request.session.get("active_company_id")
    today = timezone.now().date()

    # ============================
    # STOCK TOTAL (UNIDADES)
    # ============================
    total_stock_units = (
        InventoryItem.objects.filter(company_id=company_id)
        .aggregate(total=Sum("quantity"))["total"] or 0
    )

    # ============================
    # STOCK VALORIZADO
    # ============================
    total_stock_value = (
        InventoryItem.objects.filter(company_id=company_id)
        .annotate(value=F("quantity") * F("product__cost"))
        .aggregate(total=Sum("value"))["total"] or 0
    )

    # ============================
    # PRODUCTOS BAJO STOCK MÍNIMO
    # ============================
    low_stock_count = (
        InventoryItem.objects.filter(
            company_id=company_id,
            quantity__lt=F("min_stock")
        ).count()
    )

    # ============================
    # PRODUCTOS SIN MOVIMIENTO 60 DÍAS
    # ============================
    last_60 = today - timezone.timedelta(days=60)

    no_movement_60_days = (
        InventoryItem.objects.filter(company_id=company_id)
        .exclude(movements__date__gte=last_60)
        .count()
    )

    # ============================
    # MOVIMIENTOS DEL DÍA
    # ============================
    mov_in_today = InventoryMovement.objects.filter(
        company_id=company_id,
        movement_type="IN",
        date=today
    ).aggregate(total=Sum("quantity"))["total"] or 0

    mov_out_today = InventoryMovement.objects.filter(
        company_id=company_id,
        movement_type="OUT",
        date=today
    ).aggregate(total=Sum("quantity"))["total"] or 0

    mov_total_today = mov_in_today + mov_out_today

    # ============================
    # ROTACIÓN POR CATEGORÍA (OUT)
    # ============================
    rotation_by_category = (
        InventoryMovement.objects.filter(
            company_id=company_id,
            movement_type="OUT"
        )
        .values("item__product__category__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")
    )

    # ============================
    # TOP PRODUCTOS OUT DEL DÍA
    # ============================
    top_products_out_today = (
        InventoryMovement.objects.filter(
            company_id=company_id,
            movement_type="OUT",
            date=today
        )
        .values("item__product__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:10]
    )

    # ============================
    # TOP PROVEEDORES IN DEL DÍA
    # ============================
    top_suppliers_in_today = (
        PurchaseLine.objects.filter(
            purchase__company_id=company_id,
            purchase__date=today
        )
        .values("purchase__supplier__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:10]
    )

    # ============================
    # MOVIMIENTOS POR HORA
    # ============================
    mov_by_hour_today = (
        InventoryMovement.objects.filter(
            company_id=company_id,
            date=today
        )
        .values("created_at__hour")
        .annotate(total=Sum("quantity"))
        .order_by("created_at__hour")
    )

    context = {
        "total_stock_units": total_stock_units,
        "total_stock_value": total_stock_value,
        "low_stock_count": low_stock_count,
        "no_movement_60_days": no_movement_60_days,
        "mov_in_today": mov_in_today,
        "mov_out_today": mov_out_today,
        "mov_total_today": mov_total_today,
        "rotation_by_category": rotation_by_category,
        "top_products_out_today": top_products_out_today,
        "top_suppliers_in_today": top_suppliers_in_today,
        "mov_by_hour_today": mov_by_hour_today,
    }

    return render(request, "reports/inventory_dashboard.html", context)
