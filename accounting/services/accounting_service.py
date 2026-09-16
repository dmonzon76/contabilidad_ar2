from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
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
    @transaction.atomic
    def post_sale(sale):
        company = sale.company
        period = AccountingService.get_period(company, sale.date)

        # 1. Identificar si es venta de servicios o mercaderías
        is_service = getattr(sale, 'is_service', False) or getattr(sale, 'sale_type', '') == 'SERVICE'

        # 2. Creación de la cabecera del asiento
        entry = JournalEntry.objects.create(
            company=company,
            period=period,
            date=sale.date,
            description=f"Factura fiscal {sale.number}",
            created_by=getattr(sale, "created_by", None),
        )

        # 3. DEBE: Cliente / Deudores por Ventas (Total del comprobante)
        account_client = Account.objects.get(company=company, code="CLIENTES")
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_client,
            debit=sale.total_amount,
            credit=0,
            description=f"Cliente {sale.customer.name}",
        )

        # 4. HABER: Cuenta de Ventas (Neto Gravado)
        sales_code = "VENTAS_SERVICIOS" if is_service else "VENTAS"
        try:
            account_sales = Account.objects.get(company=company, code=sales_code)
        except Account.DoesNotExist:
            account_sales = Account.objects.get(company=company, code="VENTAS")

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_sales,
            debit=0,
            credit=sale.net_amount,
            description="Venta de servicios" if is_service else "Ventas netas de mercaderías",
        )

        # 5. HABER: IVA Débito Fiscal
        iva_amount = getattr(sale, 'iva_amount', 0) or getattr(sale, 'vat_amount', 0)
        if iva_amount > 0:
            account_iva = Account.objects.get(company=company, code="IVA_DEBITO")
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_iva,
                debit=0,
                credit=iva_amount,
                description="IVA débito fiscal",
            )

        # 6. HABER: Percepción de Ingresos Brutos (Pasivo a depositar)
        iibb_amount = getattr(sale, 'iibb_perception_amount', 0)
        if iibb_amount > 0:
            account_iibb = Account.objects.get(company=company, code="PERCEPCION_IIBB_A_DEPOSITAR")
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_iibb,
                debit=0,
                credit=iibb_amount,
                description="Percepción IIBB practicada",
            )

        # 7. HABER: Percepción de IVA (Pasivo a depositar)
        vat_perc_amount = getattr(sale, 'vat_perception_amount', 0)
        if vat_perc_amount > 0:
            account_vat_perc = Account.objects.get(company=company, code="PERCEPCION_IVA_A_DEPOSITAR")
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_vat_perc,
                debit=0,
                credit=vat_perc_amount,
                description="Percepción IVA practicada",
            )

        # 8. DEBE/HABER: CMV + Inventario (Solo si es bienes de cambio y tiene costo > 0)
        total_cost = getattr(sale, 'total_cost', 0)
        if not is_service and total_cost > 0:
            account_cmv = Account.objects.get(company=company, code="CMV")
            account_inventory = Account.objects.get(company=company, code="INVENTARIO")

            JournalEntryLine.objects.create(
                entry=entry,
                account=account_cmv,
                debit=total_cost,
                credit=0,
                description="Costo de mercadería vendida",
            )

            JournalEntryLine.objects.create(
                entry=entry,
                account=account_inventory,
                debit=0,
                credit=total_cost,
                description="Salida de inventario",
            )

        return entry