from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count

from company.models import Company
from sales.models.sale import Sale
from purchases.models.purchase import Purchase
from inventory.models import InventoryMovement
from accounting.models import JournalEntry
from accounting.models.account_movement import AccountMovement
from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    company_id = request.session.get("active_company_id")
    today = timezone.now().date()

    company = get_object_or_404(Company, pk=company_id)

    # Sales
    sales_qs = Sale.objects.filter(company_id=company_id, date=today)
    sales_total = sales_qs.aggregate(total=Sum("total_amount"))["total"] or 0
    sales_count = sales_qs.count()
    iva_debit_today = sales_qs.aggregate(total=Sum("iva_amount"))["total"] or 0
    cmv_today = sales_qs.aggregate(total=Sum("total_cost"))["total"] or 0
    profit_today = sales_total - cmv_today

    # Purchases
    purchases_qs = Purchase.objects.filter(company_id=company_id, date=today)
    purchases_total = purchases_qs.aggregate(total=Sum("total_amount"))["total"] or 0
    purchases_count = purchases_qs.count()
    iva_credit_today = purchases_qs.aggregate(total=Sum("tax_amount"))["total"] or 0

    # Inventory movements
    inventory_movements_today = InventoryMovement.objects.filter(
        company_id=company_id,
        date=today
    ).count()

    # Journal entries
    journal_today = JournalEntry.objects.filter(
        company_id=company_id,
        date=today
    ).count()

    # Account balances
    cc_customers_balance = (
        AccountMovement.objects.filter(
            company_id=company_id,
            customer__isnull=False
        ).aggregate(total=Sum("amount"))["total"] or 0
    )

    cc_suppliers_balance = (
        AccountMovement.objects.filter(
            company_id=company_id,
            supplier__isnull=False
        ).aggregate(total=Sum("amount"))["total"] or 0
    )

    context = {
        "company": company,
        "sales_total": sales_total,
        "sales_count": sales_count,
        "purchases_total": purchases_total,
        "purchases_count": purchases_count,
        "iva_debit_today": iva_debit_today,
        "iva_credit_today": iva_credit_today,
        "cmv_today": cmv_today,
        "profit_today": profit_today,
        "inventory_movements_today": inventory_movements_today,
        "journal_today": journal_today,
        "cc_customers_balance": cc_customers_balance,
        "cc_suppliers_balance": cc_suppliers_balance,
    }

    return render(request, "core/dashboard.html", context)
