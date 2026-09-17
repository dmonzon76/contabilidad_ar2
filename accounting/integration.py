from django.utils import timezone
from accounting.models import JournalEntry, JournalEntryLine, Account
from accounting.models.account_movement import AccountMovement
from accounting.models.period import Period
from accounting.services import AccountingService


def get_period_for_purchase(purchase):
    """
    Devuelve el período contable correspondiente a la fecha de la compra.
    """
    return Period.objects.get(
        fiscal_year__company=purchase.company,
        start_date__lte=purchase.date,
        end_date__gte=purchase.date,
        status="OPEN",
    )


# ============================================================
# UTILIDAD
# ============================================================


def get_account(company, code):
    return Account.objects.get(company=company, code=code)


# ============================================================
# ASIENTOS AUTOMÁTICOS DE COMPRAS
# ============================================================


def create_purchase_journal_entry(purchase):
    """Backward-compatible wrapper around the centralized accounting service."""
    return AccountingService.post_purchase(purchase)


def delete_journal_entries_for_purchase(purchase):
    JournalEntry.objects.filter(
        company=purchase.company,
        description__icontains=f"Compra {purchase.invoice_number}",
    ).delete()


# ============================================================
# ASIENTOS AUTOMÁTICOS DE VENTAS
# ============================================================


def create_sale_journal_entry(sale):
    """Backward-compatible wrapper around the centralized accounting service."""
    return AccountingService.post_sale(sale)


def delete_journal_entries_for_sale(sale):
    JournalEntry.objects.filter(
        company=sale.company, description__icontains=f"Venta {sale.number}"
    ).delete()


# ============================================================
# CMV
# ============================================================


def create_cmv_journal_entry(sale):
    """Backward-compatible wrapper. CMV is included inside the main sale entry."""
    return AccountingService.post_sale(sale)


def delete_cmv_journal_entry(sale):
    JournalEntry.objects.filter(
        company=sale.company, description__icontains=f"CMV Venta {sale.number}"
    ).delete()


# ============================================================
# CUENTA CORRIENTE CLIENTES
# ============================================================


def create_customer_cc_from_sale(sale):
    AccountMovement.objects.create(
        company=sale.company,
        customer=sale.customer,
        sale=sale,
        movement_type="DEBIT",
        amount=sale.total_amount,
        description=f"Venta {sale.number}",
    )


def delete_customer_cc_from_sale(sale):
    AccountMovement.objects.filter(company=sale.company, sale=sale).delete()


# ============================================================
# CUENTA CORRIENTE PROVEEDORES
# ============================================================


def create_supplier_cc_from_purchase(purchase):
    AccountMovement.objects.create(
        company=purchase.company,
        supplier=purchase.supplier,
        purchase=purchase,
        movement_type="CREDIT",
        amount=purchase.total_amount,
        description=f"Compra {purchase.invoice_number}",
    )


def delete_supplier_cc_from_purchase(purchase):
    AccountMovement.objects.filter(company=purchase.company, purchase=purchase).delete()
