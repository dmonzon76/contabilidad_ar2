from django.utils import timezone
from accounting.models import JournalEntry, JournalEntryLine, Account
from accounting.models.account_movement import AccountMovement


# ============================================================
# UTILIDAD
# ============================================================

def get_account(company, code):
    return Account.objects.get(company=company, code=code)


# ============================================================
# ASIENTOS AUTOMÁTICOS DE COMPRAS
# ============================================================

def create_purchase_journal_entry(purchase):
    company = purchase.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"Compra {purchase.invoice_number}",
    )

    acc_inventory = get_account(company, "1.1.09")
    acc_iva_credit = get_account(company, "7.2")
    acc_prov = get_account(company, "2.1.01")

    JournalEntryLine.objects.create(entry=entry, account=acc_inventory,
                                    debit=purchase.net_amount, credit=0)

    JournalEntryLine.objects.create(entry=entry, account=acc_iva_credit,
                                    debit=purchase.vat_amount, credit=0)

    JournalEntryLine.objects.create(entry=entry, account=acc_prov,
                                    debit=0, credit=purchase.total_amount)

    return entry


def delete_journal_entries_for_purchase(purchase):
    JournalEntry.objects.filter(
        company=purchase.company,
        description__icontains=f"Compra {purchase.invoice_number}"
    ).delete()


# ============================================================
# ASIENTOS AUTOMÁTICOS DE VENTAS
# ============================================================

def create_sale_journal_entry(sale):
    company = sale.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"Venta {sale.number}",
    )

    acc_clients = get_account(company, "1.1.04")
    acc_sales = get_account(company, "4.1.01")
    acc_iva_debit = get_account(company, "7.1")

    JournalEntryLine.objects.create(entry=entry, account=acc_clients,
                                    debit=sale.total_amount, credit=0)

    JournalEntryLine.objects.create(entry=entry, account=acc_sales,
                                    debit=0, credit=sale.net_amount)

    JournalEntryLine.objects.create(entry=entry, account=acc_iva_debit,
                                    debit=0, credit=sale.vat_amount)

    return entry


def delete_journal_entries_for_sale(sale):
    JournalEntry.objects.filter(
        company=sale.company,
        description__icontains=f"Venta {sale.number}"
    ).delete()


# ============================================================
# CMV
# ============================================================

def create_cmv_journal_entry(sale):
    company = sale.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"CMV Venta {sale.number}",
    )

    acc_cmv = get_account(company, "5.1.01")
    acc_inventory = get_account(company, "1.1.09")

    JournalEntryLine.objects.create(entry=entry, account=acc_cmv,
                                    debit=sale.cost_total, credit=0)

    JournalEntryLine.objects.create(entry=entry, account=acc_inventory,
                                    debit=0, credit=sale.cost_total)

    return entry


def delete_cmv_journal_entry(sale):
    JournalEntry.objects.filter(
        company=sale.company,
        description__icontains=f"CMV Venta {sale.number}"
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
    AccountMovement.objects.filter(
        company=sale.company,
        sale=sale
    ).delete()


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
    AccountMovement.objects.filter(
        company=purchase.company,
        purchase=purchase
    ).delete()
