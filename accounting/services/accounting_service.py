from django.core.exceptions import ValidationError
from django.utils import timezone

from accounting.models import (
    JournalEntry,
    JournalEntryLine,
    Account,
    Period,
)


class AccountingService:

    @staticmethod
    def get_period(company, date=None):
        date = date or timezone.now().date()
        try:
            return Period.objects.get(
                fiscal_year__company=company,
                start_date__lte=date,
                end_date__gte=date,
                status="OPEN",
            )
        except Period.DoesNotExist:
            raise ValidationError("No open accounting period for this date.")

    @staticmethod
    def post_sale(sale):
        # IMPORT LOCAL (evita circular import)
        # from sales.models.sale import Sale   ← NO NECESARIO

        company = sale.company
        period = AccountingService.get_period(company, sale.date)

        entry = JournalEntry.objects.create(
            company=company,
            period=period,
            date=sale.date,
            description=f"Factura fiscal {sale.number}",
            created_by=getattr(sale, "created_by", None),
        )

        # Cliente (DEBE)
        account_client = Account.objects.get(company=company, code="CLIENTES")
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_client,
            debit=sale.total_amount,
            description=f"Cliente {sale.customer.name}",
        )

        # Ventas (HABER)
        account_sales = Account.objects.get(company=company, code="VENTAS")
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_sales,
            credit=sale.net_amount,
            description="Ventas netas",
        )

        # IVA Débito Fiscal (HABER)
        account_iva = Account.objects.get(company=company, code="IVA_DEBITO")
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_iva,
            credit=sale.iva_amount,
            description="IVA débito fiscal",
        )

        # CMV + Inventario (solo si hay mercadería)
        if sale.total_cost > 0:
            account_cmv = Account.objects.get(company=company, code="CMV")
            account_inventory = Account.objects.get(company=company, code="INVENTARIO")

            JournalEntryLine.objects.create(
                entry=entry,
                account=account_cmv,
                debit=sale.total_cost,
                description="Costo de mercadería vendida",
            )

            JournalEntryLine.objects.create(
                entry=entry,
                account=account_inventory,
                credit=sale.total_cost,
                description="Salida de inventario",
            )

        return entry

    @staticmethod
    def post_purchase(purchase):
        # IMPORT LOCAL (evita circular import)
        # from purchases.models.purchase import Purchase   ← NO NECESARIO

        company = purchase.company
        period = AccountingService.get_period(company, purchase.date)

        entry = JournalEntry.objects.create(
            company=company,
            period=period,
            date=purchase.date,
            description=f"Compra {purchase.invoice_number}",
            created_by=getattr(purchase, "created_by", None),
        )

        account_supplier = Account.objects.get(company=company, code="PROVEEDORES")
        account_expense = Account.objects.get(company=company, code="GASTOS")
        account_iva = Account.objects.get(company=company, code="IVA_CREDITO")

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_expense,
            debit=purchase.net_amount,
            description="Gasto por compra",
        )

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_iva,
            debit=purchase.tax_amount,
            description="IVA crédito fiscal",
        )

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_supplier,
            credit=purchase.total_amount,
            description=f"Proveedor {purchase.supplier.name}",
        )

        return entry

    @staticmethod
    def reverse_entry(entry):
        company = entry.company
        period = AccountingService.get_period(company, timezone.now().date())

        reverse = JournalEntry.objects.create(
            company=company,
            period=period,
            date=timezone.now().date(),
            description=f"Reverso de asiento #{entry.id}",
            created_by=entry.created_by,
        )

        for line in entry.lines.all():
            JournalEntryLine.objects.create(
                entry=reverse,
                account=line.account,
                debit=line.credit,
                credit=line.debit,
                description=f"Reverso de línea {line.id}",
            )

        return reverse
