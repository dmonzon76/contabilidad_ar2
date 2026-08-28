# accounting/services/generate_entry.py

from accounting.models.journal import JournalEntry, JournalEntryLine
from accounting.models.account import Account
from accounting.models.period import Period
from fiscal.models import FiscalInvoiceLine



def get_account(company, code):
    return Account.objects.get(company=company, code=code)


def current_period(company):
    return Period.objects.get_current(company=company)


def generate_accounting_entry(invoice, user):
    """
    Genera asiento contable automático basado en:
    - líneas de factura
    - impuestos (Tax)
    - cuentas contables definidas en Tax.account_code
    """

    company = invoice.company
    period = current_period(company)

    entry = JournalEntry.objects.create(
        company=company,
        period=period,
        date=invoice.date,
        description=f"Fiscal sale {invoice.voucher_number}",
        created_by=user,
    )

    # 1) Cobro (Caja)
    cash_account = get_account(company, "CAJA")
    JournalEntryLine.objects.create(
        entry=entry,
        account=cash_account,
        debit=invoice.total,
        description="Cobro de venta fiscal",
    )

    # 2) Líneas de factura
    lines = FiscalInvoiceLine.objects.filter(invoice=invoice)

    for line in lines:
        total_line = line.line_total()
        tax = line.tax

        # Cuenta de ventas (puede ser parametrizable por producto)
        sales_account = get_account(company, "VENTAS")

        if tax.is_vat:
            base_amount = total_line
            vat_amount = total_line * (tax.rate / 100)

            # Ventas gravadas
            JournalEntryLine.objects.create(
                entry=entry,
                account=sales_account,
                credit=base_amount,
                description=f"Venta gravada {tax.rate}%",
            )

            # IVA Débito
            if tax.account_code:
                vat_account = get_account(company, tax.account_code)
                JournalEntryLine.objects.create(
                    entry=entry,
                    account=vat_account,
                    credit=vat_amount,
                    description=f"IVA Débito {tax.rate}%",
                )

        elif tax.is_exempt:
            JournalEntryLine.objects.create(
                entry=entry,
                account=sales_account,
                credit=total_line,
                description="Venta exenta",
            )

        elif tax.is_non_taxed:
            JournalEntryLine.objects.create(
                entry=entry,
                account=sales_account,
                credit=total_line,
                description="Venta no gravada",
            )

        else:
            # Percepciones, retenciones, impuestos internos
            if tax.account_code:
                tax_account = get_account(company, tax.account_code)
                JournalEntryLine.objects.create(
                    entry=entry,
                    account=tax_account,
                    credit=total_line,
                    description=f"Impuesto {tax.name}",
                )

    # 3) CMV y baja de stock
    sale = invoice.sale
    if sale.total_cost > 0:
        cmv_account = get_account(company, "CMV")
        stock_account = get_account(company, "MERCADERIAS")

        JournalEntryLine.objects.create(
            entry=entry,
            account=cmv_account,
            debit=sale.total_cost,
            description="Costo de mercaderías vendidas",
        )

        JournalEntryLine.objects.create(
            entry=entry,
            account=stock_account,
            credit=sale.total_cost,
            description="Baja de stock por venta",
        )

    return entry
