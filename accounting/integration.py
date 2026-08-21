from accounting.models import JournalEntry, JournalEntryLine, Account
from django.utils import timezone
from accounting.models import JournalEntry, JournalEntryLine, Account
from django.utils import timezone

def get_account(company, code):
    return Account.objects.get(company=company, code=code)


# ============================================================
# ASIENTO AUTOMÁTICO DE COMPRAS
# ============================================================

def create_purchase_journal_entry(purchase):
    company = purchase.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"Compra {purchase.invoice_number}",
    )

    # 1) Mercaderías (DEBE)
    acc_merch = get_account(company, "1.1.4.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_merch,
        debit=purchase.net_amount,
        credit=0,
    )

    # 2) IVA Crédito Fiscal (DEBE)
    acc_iva_credit = get_account(company, "1.1.3.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_iva_credit,
        debit=purchase.vat_amount,
        credit=0,
    )

    # 3) Proveedores (HABER)
    acc_prov = get_account(company, "2.1.1.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_prov,
        debit=0,
        credit=purchase.total_amount,
    )

    return entry


# ============================================================
# ASIENTO AUTOMÁTICO DE VENTAS
# ============================================================

def create_sale_journal_entry(sale):
    company = sale.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"Venta {sale.number}",
    )

    # 1) Clientes (DEBE)
    acc_clients = get_account(company, "1.1.2.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_clients,
        debit=sale.total_amount,
        credit=0,
    )

    # 2) Ventas de Mercaderías (HABER)
    acc_sales = get_account(company, "4.1.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_sales,
        debit=0,
        credit=sale.net_amount,
    )

    # 3) IVA Débito Fiscal (HABER)
    acc_iva_debit = get_account(company, "2.1.2.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_iva_debit,
        debit=0,
        credit=sale.vat_amount,
    )

    return entry


# ============================================================
# ASIENTO AUTOMÁTICO DE CMV
# ============================================================

def create_cmv_journal_entry(sale):
    company = sale.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"CMV Venta {sale.number}",
    )

    # 1) CMV (DEBE)
    acc_cmv = get_account(company, "5.3")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_cmv,
        debit=sale.cost_total,
        credit=0,
    )

    # 2) Mercaderías (HABER)
    acc_merch = get_account(company, "1.1.4.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_merch,
        debit=0,
        credit=sale.cost_total,
    )

    return entry





def get_account(company, code):
    return Account.objects.get(company=company, code=code)


# ============================================================
# ASIENTO AUTOMÁTICO DE VENTAS
# ============================================================

def create_sale_journal_entry(sale):
    company = sale.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"Venta {sale.number}",
    )

    # 1) Clientes (DEBE)
    acc_clients = get_account(company, "1.1.2.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_clients,
        debit=sale.total_amount,
        credit=0,
    )

    # 2) Ventas de Mercaderías (HABER)
    acc_sales = get_account(company, "4.1.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_sales,
        debit=0,
        credit=sale.net_amount,
    )

    # 3) IVA Débito Fiscal (HABER)
    acc_iva_debit = get_account(company, "2.1.2.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_iva_debit,
        debit=0,
        credit=sale.vat_amount,
    )

    return entry


# ============================================================
# ASIENTO AUTOMÁTICO DE CMV
# ============================================================

def create_cmv_journal_entry(sale):
    company = sale.company

    entry = JournalEntry.objects.create(
        company=company,
        date=timezone.now(),
        description=f"CMV Venta {sale.number}",
    )

    # 1) CMV (DEBE)
    acc_cmv = get_account(company, "5.3")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_cmv,
        debit=sale.cost_total,
        credit=0,
    )

    # 2) Mercaderías (HABER)
    acc_merch = get_account(company, "1.1.4.01")
    JournalEntryLine.objects.create(
        entry=entry,
        account=acc_merch,
        debit=0,
        credit=sale.cost_total,
    )

    return entry
