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
    def ensure_required_accounts(company):
        required_accounts = [
            ("CAJA", "Caja", "ASSET"),
            ("CLIENTES", "Clientes", "ASSET"),
            ("VENTAS", "Ventas", "INCOME"),
            ("VENTAS_SERVICIOS", "Ventas de Servicios", "INCOME"),
            ("IVA_DEBITO", "IVA Débito Fiscal", "LIABILITY"),
            ("CMV", "Costo de Mercaderías Vendidas", "EXPENSE"),
            ("INVENTARIO", "Inventario", "ASSET"),
            ("PROVEEDORES", "Proveedores", "LIABILITY"),
            ("GASTOS", "Gastos", "EXPENSE"),
            ("IVA_CREDITO", "IVA Crédito Fiscal", "LIABILITY"),
            ("PERCEPCION_IIBB_A_DEPOSITAR", "Percepción IIBB a depositar", "LIABILITY"),
            ("PERCEPCION_IVA_A_DEPOSITAR", "Percepción IVA a depositar", "LIABILITY"),
        ]

        created = []
        for code, name, account_type in required_accounts:
            account, was_created = Account.objects.get_or_create(
                company=company,
                code=code,
                defaults={
                    "name": name,
                    "account_type": account_type,
                },
            )
            if was_created:
                created.append(account.code)

        return created

    @staticmethod
    def get_or_create_account(company, code, name, account_type):
        return Account.objects.get_or_create(
            company=company,
            code=code,
            defaults={
                "name": name,
                "account_type": account_type,
            },
        )[0]

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
    def _existing_entry(company, description):
        return (
            JournalEntry.objects.filter(
                company=company,
                description=description,
            )
            .order_by("-id")
            .first()
        )

    @staticmethod
    @transaction.atomic
    def post_purchase(purchase):
        company = purchase.company
        period = AccountingService.get_period(company, purchase.date)
        description = f"Compra {purchase.invoice_number}"

        existing = AccountingService._existing_entry(company, description)
        if existing:
            return existing

        entry = JournalEntry.objects.create(
            company=company,
            period=period,
            date=purchase.date,
            description=description,
            created_by=getattr(purchase, "created_by", None),
        )

        account_inventory = AccountingService.get_or_create_account(
            company,
            "INVENTARIO",
            "Inventario",
            "ASSET",
        )
        account_iva_credit = AccountingService.get_or_create_account(
            company,
            "IVA_CREDITO",
            "IVA Crédito Fiscal",
            "LIABILITY",
        )
        account_prov = AccountingService.get_or_create_account(
            company,
            "PROVEEDORES",
            "Proveedores",
            "LIABILITY",
        )

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_inventory,
            debit=purchase.net_amount,
            credit=0,
            description="Compra de mercadería",
        )

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_iva_credit,
            debit=purchase.tax_amount,
            credit=0,
            description="IVA crédito fiscal",
        )

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_prov,
            debit=0,
            credit=purchase.total_amount,
            description="Proveedor",
        )

        return entry

    @staticmethod
    @transaction.atomic
    def post_fiscal_invoice(invoice):
        company = invoice.company
        entry_date = invoice.date or timezone.localdate()
        period = AccountingService.get_period(company, entry_date)
        description = f"Factura fiscal {invoice.number}"

        existing = AccountingService._existing_entry(company, description)
        if existing:
            return existing

        entry = JournalEntry.objects.create(
            company=company,
            period=period,
            date=entry_date,
            description=description,
            created_by=getattr(invoice, "created_by", None),
        )

        account_cash = AccountingService.get_or_create_account(
            company,
            "CAJA",
            "Caja",
            "ASSET",
        )
        account_sales = AccountingService.get_or_create_account(
            company,
            "VENTAS",
            "Ventas",
            "INCOME",
        )
        account_tax = AccountingService.get_or_create_account(
            company,
            "IVA_DEBITO",
            "IVA Débito Fiscal",
            "LIABILITY",
        )

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_cash,
            debit=invoice.total_amount,
            credit=0,
            description="Cobro de factura fiscal",
        )
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_sales,
            debit=0,
            credit=invoice.net_amount,
            description="Venta de factura fiscal",
        )
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_tax,
            debit=0,
            credit=invoice.tax_amount,
            description="Impuestos de factura fiscal",
        )

        return entry

    @staticmethod
    @transaction.atomic
    def post_sale(sale):
        company = sale.company
        period = AccountingService.get_period(company, sale.date)
        description = f"Venta {sale.number}"

        existing = AccountingService._existing_entry(company, description)
        if existing:
            return existing

        # 1. Identificar si es venta de servicios o mercaderías
        is_service = (
            getattr(sale, "is_service", False)
            or getattr(sale, "sale_type", "") == "SERVICE"
        )

        # 2. Creación de la cabecera del asiento
        entry = JournalEntry.objects.create(
            company=company,
            period=period,
            date=sale.date,
            description=description,
            created_by=getattr(sale, "created_by", None),
        )

        # 3. DEBE: Cliente / Deudores por Ventas (Total del comprobante)
        account_client = AccountingService.get_or_create_account(
            company,
            "CLIENTES",
            "Clientes",
            "ASSET",
        )
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
            account_sales = AccountingService.get_or_create_account(
                company,
                sales_code,
                "Ventas de Servicios" if is_service else "Ventas",
                "INCOME",
            )

        JournalEntryLine.objects.create(
            entry=entry,
            account=account_sales,
            debit=0,
            credit=sale.net_amount,
            description=(
                "Venta de servicios" if is_service else "Ventas netas de mercaderías"
            ),
        )

        # 5. HABER: IVA Débito Fiscal
        iva_amount = getattr(sale, "iva_amount", 0) or getattr(sale, "vat_amount", 0)
        if iva_amount > 0:
            account_iva = AccountingService.get_or_create_account(
                company,
                "IVA_DEBITO",
                "IVA Débito Fiscal",
                "LIABILITY",
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_iva,
                debit=0,
                credit=iva_amount,
                description="IVA débito fiscal",
            )

        # 6. HABER: Percepción de Ingresos Brutos (Pasivo a depositar)
        iibb_amount = getattr(sale, "iibb_perception_amount", 0)
        if iibb_amount > 0:
            account_iibb = AccountingService.get_or_create_account(
                company,
                "PERCEPCION_IIBB_A_DEPOSITAR",
                "Percepción IIBB a depositar",
                "LIABILITY",
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_iibb,
                debit=0,
                credit=iibb_amount,
                description="Percepción IIBB practicada",
            )

        # 7. HABER: Percepción de IVA (Pasivo a depositar)
        vat_perc_amount = getattr(sale, "vat_perception_amount", 0)
        if vat_perc_amount > 0:
            account_vat_perc = AccountingService.get_or_create_account(
                company,
                "PERCEPCION_IVA_A_DEPOSITAR",
                "Percepción IVA a depositar",
                "LIABILITY",
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_vat_perc,
                debit=0,
                credit=vat_perc_amount,
                description="Percepción IVA practicada",
            )

        # 8. DEBE/HABER: CMV + Inventario (Solo si es bienes de cambio y tiene costo > 0)
        total_cost = getattr(sale, "total_cost", 0)
        if not is_service and total_cost > 0:
            account_cmv = AccountingService.get_or_create_account(
                company,
                "CMV",
                "Costo de Mercaderías Vendidas",
                "EXPENSE",
            )
            account_inventory = AccountingService.get_or_create_account(
                company,
                "INVENTARIO",
                "Inventario",
                "ASSET",
            )

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
