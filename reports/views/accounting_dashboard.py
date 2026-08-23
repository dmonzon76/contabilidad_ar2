from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone

from accounting.models import JournalEntry, JournalEntryLine, Account
from sales.models.sale import Sale
from purchases.models.purchase import Purchase


def accounting_dashboard(request):
    company_id = request.session.get("active_company_id")
    today = timezone.now().date()

    # ============================
    # ASIENTOS DEL DÍA
    # ============================
    journal_entries_today = JournalEntry.objects.filter(
        company_id=company_id,
        date=today
    )

    journal_lines_today = JournalEntryLine.objects.filter(
        entry__company_id=company_id,
        entry__date=today
    )

    # ============================
    # IVA DÉBITO (VENTAS)
    # ============================
    iva_debit_today = (
        Sale.objects.filter(company_id=company_id, date=today)
        .aggregate(total=Sum("vat_amount"))["total"] or 0
    )

    # ============================
    # IVA CRÉDITO (COMPRAS)
    # ============================
    iva_credit_today = (
        Purchase.objects.filter(company_id=company_id, date=today)
        .aggregate(total=Sum("vat_amount"))["total"] or 0
    )

    # ============================
    # CMV DEL DÍA
    # ============================
    cmv_today = (
        Sale.objects.filter(company_id=company_id, date=today)
        .aggregate(total=Sum("cost_total"))["total"] or 0
    )

    # ============================
    # RESULTADO DEL DÍA
    # ============================
    sales_today_total = (
        Sale.objects.filter(company_id=company_id, date=today)
        .aggregate(total=Sum("total_amount"))["total"] or 0
    )

    profit_today = sales_today_total - cmv_today

    # ============================
    # TOP CUENTAS DEL DÍA
    # ============================
    top_accounts_today = (
        journal_lines_today
        .values("account__name")
        .annotate(
            debit_total=Sum("debit"),
            credit_total=Sum("credit")
        )
        .order_by("-debit_total", "-credit_total")[:10]
    )

    # ============================
    # MOVIMIENTOS POR TIPO DE CUENTA
    # ============================
    journal_by_account_type_today = (
        journal_lines_today
        .values("account__type")
        .annotate(
            debit_total=Sum("debit"),
            credit_total=Sum("credit")
        )
        .order_by("account__type")
    )

    # ============================
    # MOVIMIENTOS POR HORA
    # ============================
    journal_by_hour_today = (
        journal_entries_today
        .values("created_at__hour")
        .annotate(total=Count("id"))
        .order_by("created_at__hour")
    )

    # ============================
    # BALANCE PARCIAL DEL DÍA
    # ============================
    balance_today_debit = journal_lines_today.aggregate(total=Sum("debit"))["total"] or 0
    balance_today_credit = journal_lines_today.aggregate(total=Sum("credit"))["total"] or 0

    context = {
        "journal_entries_today": journal_entries_today.count(),
        "journal_lines_today": journal_lines_today.count(),
        "iva_debit_today": iva_debit_today,
        "iva_credit_today": iva_credit_today,
        "cmv_today": cmv_today,
        "profit_today": profit_today,
        "top_accounts_today": top_accounts_today,
        "journal_by_account_type_today": journal_by_account_type_today,
        "journal_by_hour_today": journal_by_hour_today,
        "balance_today_debit": balance_today_debit,
        "balance_today_credit": balance_today_credit,
    }

    return render(request, "reports/accounting_dashboard.html", context)
