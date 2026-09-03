from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone

from accounting.models.account_movement import AccountMovement


def cc_dashboard(request):
    company_id = request.session.get("active_company_id")
    today = timezone.now().date()

    # ============================
    # SALDO TOTAL CLIENTES
    # ============================
    cc_customers_total = (
        AccountMovement.objects.filter(
            company_id=company_id, customer__isnull=False
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    # ============================
    # SALDO TOTAL PROVEEDORES
    # ============================
    cc_suppliers_total = (
        AccountMovement.objects.filter(
            company_id=company_id, supplier__isnull=False
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    # ============================
    # MOVIMIENTOS DEL DÍA
    # ============================
    cc_movements_today = AccountMovement.objects.filter(
        company_id=company_id, date=today
    )

    cc_movements_today_count = cc_movements_today.count()

    # ============================
    # MOVIMIENTOS POR TIPO (DEBIT / CREDIT)
    # ============================
    cc_movements_by_type_today = (
        cc_movements_today.values("movement_type")
        .annotate(total=Sum("amount"))
        .order_by("movement_type")
    )

    # ============================
    # MOVIMIENTOS POR HORA
    # ============================
    cc_movements_by_hour_today = (
        cc_movements_today.values("created_at__hour")
        .annotate(total=Sum("amount"))
        .order_by("created_at__hour")
    )

    # ============================
    # TOP DEUDORES (CLIENTES)
    # ============================
    top_customers_debt = (
        AccountMovement.objects.filter(company_id=company_id, customer__isnull=False)
        .values("customer__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:10]
    )

    # ============================
    # TOP ACREEDORES (PROVEEDORES)
    # ============================
    top_suppliers_credit = (
        AccountMovement.objects.filter(company_id=company_id, supplier__isnull=False)
        .values("supplier__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:10]
    )

    # ============================
    # ANTIGÜEDAD DE SALDOS CLIENTES
    # ============================
    customers_aging = (
        AccountMovement.objects.filter(company_id=company_id, customer__isnull=False)
        .values("customer__name")
        .annotate(last_movement=Sum("amount"), oldest=Count("id"))
        .order_by("-last_movement")
    )

    # ============================
    # ANTIGÜEDAD DE SALDOS PROVEEDORES
    # ============================
    suppliers_aging = (
        AccountMovement.objects.filter(company_id=company_id, supplier__isnull=False)
        .values("supplier__name")
        .annotate(last_movement=Sum("amount"), oldest=Count("id"))
        .order_by("-last_movement")
    )

    context = {
        "cc_customers_total": cc_customers_total,
        "cc_suppliers_total": cc_suppliers_total,
        "cc_movements_today_count": cc_movements_today_count,
        "cc_movements_by_type_today": cc_movements_by_type_today,
        "cc_movements_by_hour_today": cc_movements_by_hour_today,
        "top_customers_debt": top_customers_debt,
        "top_suppliers_credit": top_suppliers_credit,
        "customers_aging": customers_aging,
        "suppliers_aging": suppliers_aging,
    }

    return render(request, "reports/reports/cc_dashboard.html", context)
