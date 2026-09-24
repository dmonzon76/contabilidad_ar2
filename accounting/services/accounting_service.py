from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction

from accounting.models import JournalEntry, JournalEntryLine, Account, Period


class AccountingService:
    """
    Servicio contable para la generación automática de asientos en el Libro Diario.
    Adaptado estrictamente al Plan de Cuentas existente (incluyendo chart_of_accounts_full.py,
    PLAN_DE_CUENTAS jerárquicos y configuraciones de empresa).
    NO crea cuentas automáticamente en la base de datos.
    """

    # Mapeo flexible de códigos para cada función contable
    ACCOUNT_CODE_MAP = {
        "CUSTOMERS": ["1.1.5", "1.1.02.001", "1.1.02", "CLIENTES"],
        "SALES_GOODS": ["4.1.1", "4.1.01.001", "4.1.01", "4.1", "VENTAS"],
        "SALES_SERVICES": ["4.1.2", "4.1.02.001", "4.1.02", "VENTAS_SERVICIOS"],
        "IVA_DEBIT": ["7.1.1", "2.1.02.001", "2.1.05", "7.1", "IVA_DEBITO"],
        "IVA_CREDIT": ["7.1.2", "1.1.03.002", "1.1.07", "7.2", "IVA_CREDITO"],
        "SUPPLIERS": ["2.1.1", "2.1.01.001", "2.1.01", "PROVEEDORES"],
        "INVENTORY": ["1.1.8", "1.1.04.001", "1.1.04", "1.1.09", "INVENTARIO"],
        "COGS": ["5.1.1", "5.1.01.001", "5.1.01", "5.1", "CMV"],
        "EXPENSES": ["6.1.1", "6.1.01", "6.1", "6", "GASTOS"],
        "CASH": ["1.1.1", "1.1.01.001", "1.1.01", "CAJA"],
        "IIBB_PERCEPTION_ASSET": ["7.4.1", "1.1.03.004", "1.1.08", "PERCEPCION_IIBB_SUFRIDA"],
        "IIBB_PERCEPTION_LIABILITY": ["7.4.1", "2.1.02.004", "2.1.06", "PERCEPCION_IIBB_A_DEPOSITAR"],
        "IVA_PERCEPTION_LIABILITY": ["7.1.5", "2.1.02.002", "PERCEPCION_IVA_A_DEPOSITAR"],
        "RETENTIONS_PAYABLE": ["7.4.2", "7.1.6", "2.1.02.002", "2.1.08", "RETENCIONES_A_PAGAR"],
    }

    @staticmethod
    def get_account(company, account_key, setting_field=None, custom_name=""):
        """
        Busca una cuenta contable existente en la empresa.
        1. Intenta desde AccountingSettings de la empresa (si está configurada).
        2. Intenta buscar por los códigos definidos en ACCOUNT_CODE_MAP.
        3. Si no existe, lanza un ValidationError informativo sin crear cuentas en la BD.
        """
        # 1. Configuración de la empresa
        settings = getattr(company, "accounting_settings", None)
        if settings and setting_field:
            acc = getattr(settings, setting_field, None)
            if acc:
                return acc

        # 2. Búsqueda por lista de códigos mapeados (coincidencia exacta)
        candidate_codes = AccountingService.ACCOUNT_CODE_MAP.get(account_key, [account_key])
        acc = Account.objects.filter(company=company, code__in=candidate_codes, is_active=True).first()
        if acc:
            return acc

        # 3. Fallback: Búsqueda por coincidencia parcial (icontains)
        for code in candidate_codes:
            acc = Account.objects.filter(company=company, code__icontains=code, is_active=True).first()
            if acc:
                return acc

        # 4. Error si no se encuentra la cuenta
        codes_formatted = ", ".join(candidate_codes)
        name_display = custom_name or account_key
        raise ValidationError(
            f"No se encontró la cuenta contable para '{name_display}' (códigos buscados: {codes_formatted}) "
            f"en la empresa '{company.name}'. Verifique que el Plan de Cuentas esté cargado correctamente."
        )

    @staticmethod
    def get_period(company, date=None):
        """
        Obtiene el período contable abierto para la fecha indicada.
        """
        date = date or timezone.now().date()
        try:
            return Period.objects.get(
                fiscal_year__company=company,
                start_date__lte=date,
                end_date__gte=date,
                status="OPEN",
            )
        except Period.DoesNotExist:
            raise ValidationError(f"No existe un período contable abierto para la fecha {date} en la empresa '{company.name}'.")

    @staticmethod
    def _existing_entry(company, description, *, date=None, purchase=None, source_key=None):
        """
        Verifica si ya se registró un asiento para evitar duplicados.
        """
        qs = JournalEntry.objects.filter(company=company, description=description)
        if source_key and hasattr(JournalEntry, "source_key"):
            source_entry = JournalEntry.objects.filter(source_key=source_key).first()
            if source_entry:
                return source_entry
        if purchase is not None:
            qs = qs.filter(purchase=purchase)
        if date is not None:
            qs = qs.filter(date=date)
        return qs.order_by("-id").first()

    @staticmethod
    @transaction.atomic
    def post_sale(sale):
        """
        Contabiliza una venta comercial.
        Debe: Clientes
        Haber: Ventas (Neto) + IVA Débito Fiscal + Percepciones (si aplican)
        Debe/Haber: CMV / Inventario (si es venta de bienes)
        """
        company = sale.company
        period = AccountingService.get_period(company, sale.date)
        description = f"Venta {sale.number}"

        existing = AccountingService._existing_entry(
            company, description, date=sale.date, source_key=f"sale:{sale.pk}"
        )
        if existing:
            return existing

        is_service = getattr(sale, "is_service", False) or getattr(sale, "sale_type", "") == "SERVICE"

        create_kwargs = {
            "company": company,
            "period": period,
            "date": sale.date,
            "description": description,
            "created_by": getattr(sale, "created_by", None),
        }
        if hasattr(JournalEntry, "source_key"):
            create_kwargs["source_key"] = f"sale:{sale.pk}"

        entry = JournalEntry.objects.create(**create_kwargs)

        # 1. DEBE: Clientes / Deudores por Ventas (Total de la Venta)
        account_client = AccountingService.get_account(
            company, "CUSTOMERS", "account_customers", "Clientes"
        )
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_client,
            debit=sale.total_amount,
            credit=0,
            description=f"Cliente {sale.customer.name}",
        )

        # 2. HABER: Ventas (Neto Gravado)
        sales_key = "SALES_SERVICES" if is_service else "SALES_GOODS"
        sales_setting = "account_sales_services" if is_service else "account_sales_goods"
        sales_label = "Ventas de Servicios" if is_service else "Ventas de Mercaderías"

        account_sales = AccountingService.get_account(
            company, sales_key, sales_setting, sales_label
        )
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_sales,
            debit=0,
            credit=sale.net_amount,
            description=sales_label,
        )

        # 3. HABER: IVA Débito Fiscal
        iva_amount = getattr(sale, "iva_amount", Decimal("0.00")) or getattr(sale, "vat_amount", Decimal("0.00"))
        if iva_amount > 0:
            account_iva = AccountingService.get_account(
                company, "IVA_DEBIT", "account_iva_debit", "IVA Débito Fiscal"
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_iva,
                debit=0,
                credit=iva_amount,
                description="IVA Débito Fiscal",
            )

        # 4. HABER: Percepciones IIBB Practicadas
        iibb_amount = getattr(sale, "iibb_perception_amount", Decimal("0.00"))
        if iibb_amount > 0:
            account_iibb = AccountingService.get_account(
                company, "IIBB_PERCEPTION_LIABILITY", "account_iibb_perception_payable", "Percepción IIBB a Depositar"
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_iibb,
                debit=0,
                credit=iibb_amount,
                description="Percepción IIBB practicada",
            )

        # 5. HABER: Percepciones IVA Practicadas
        vat_perc_amount = getattr(sale, "vat_perception_amount", Decimal("0.00"))
        if vat_perc_amount > 0:
            account_vat_perc = AccountingService.get_account(
                company, "IVA_PERCEPTION_LIABILITY", "account_iva_perception_payable", "Percepción IVA a Depositar"
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_vat_perc,
                debit=0,
                credit=vat_perc_amount,
                description="Percepción IVA practicada",
            )

        # 6. DEBE / HABER: Costo de Mercadería Vendida e Inventario
        total_cost = getattr(sale, "total_cost", Decimal("0.00"))
        if not is_service and total_cost > 0:
            account_cmv = AccountingService.get_account(
                company, "COGS", "account_cmv", "Costo de Mercaderías Vendidas"
            )
            account_inventory = AccountingService.get_account(
                company, "INVENTORY", "account_inventory", "Inventario / Mercaderías"
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

    @staticmethod
    @transaction.atomic
    def post_purchase(purchase):
        """
        Contabiliza una factura de compra.
        Debe: Inventario (Neto) + IVA Crédito Fiscal + Percepciones Sufridas (IIBB, IVA, etc.)
        Haber: Proveedores (Total a Pagar) + Retenciones Practicadas (si aplican)
        """
        company = purchase.company
        period = AccountingService.get_period(company, purchase.date)
        description = f"Compra {purchase.invoice_number}"

        existing = AccountingService._existing_entry(
            company, description, date=purchase.date, purchase=purchase, source_key=f"purchase:{purchase.pk}"
        )
        if existing:
            return existing

        create_kwargs = {
            "company": company,
            "period": period,
            "date": purchase.date,
            "description": description,
            "created_by": getattr(purchase, "created_by", None),
        }

        # Vincular la compra si la clave foránea existe en JournalEntry
        if hasattr(JournalEntry, "purchase"):
            create_kwargs["purchase"] = purchase
        if hasattr(JournalEntry, "source_key"):
            create_kwargs["source_key"] = f"purchase:{purchase.pk}"

        entry = JournalEntry.objects.create(**create_kwargs)

        # 1. DEBE: Inventario o Gastos (Neto Gravado)
        account_inventory = AccountingService.get_account(
            company, "INVENTORY", "account_inventory", "Inventario / Mercaderías"
        )
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_inventory,
            debit=purchase.net_amount,
            credit=0,
            description="Neto Gravado Compra",
        )

        # 2. DEBE: IVA Crédito Fiscal
        if purchase.tax_amount > 0:
            account_iva_credit = AccountingService.get_account(
                company, "IVA_CREDIT", "account_iva_credit", "IVA Crédito Fiscal"
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_iva_credit,
                debit=purchase.tax_amount,
                credit=0,
                description="IVA Crédito Fiscal",
            )

        # 3. DEBE: Percepciones Sufridas (IIBB por Jurisdicción, IVA, etc.)
        if purchase.perception_amount > 0:
            account_perception = AccountingService.get_account(
                company, "IIBB_PERCEPTION_ASSET", None, "Percepción IIBB / Impuestos Sufridos"
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_perception,
                debit=purchase.perception_amount,
                credit=0,
                description="Percepciones sufridas en compra",
            )

        # 4. HABER: Proveedores (Total a Pagar)
        account_prov = AccountingService.get_account(
            company, "SUPPLIERS", "account_suppliers", "Proveedores"
        )
        JournalEntryLine.objects.create(
            entry=entry,
            account=account_prov,
            debit=0,
            credit=purchase.total_amount,
            description=f"Proveedor {purchase.supplier.name}",
        )

        # 5. HABER: Retenciones Practicadas
        if purchase.retention_amount > 0:
            account_retention = AccountingService.get_account(
                company, "RETENTIONS_PAYABLE", "account_iibb_retention_payable", "Retenciones a Pagar"
            )
            JournalEntryLine.objects.create(
                entry=entry,
                account=account_retention,
                debit=0,
                credit=purchase.retention_amount,
                description="Retenciones practicadas",
            )

        return entry

    @staticmethod
    @transaction.atomic
    def post_fiscal_invoice(invoice):
        """
        Contabiliza un comprobante fiscal directo.
        Debe: Caja / Cobros
        Haber: Ventas + IVA Débito Fiscal
        """
        company = invoice.company
        entry_date = invoice.date or timezone.localdate()
        period = AccountingService.get_period(company, entry_date)
        description = f"Factura fiscal {invoice.number}"

        existing = AccountingService._existing_entry(
            company, description, date=entry_date, source_key=f"fiscal_invoice:{invoice.pk}"
        )
        if existing:
            return existing

        create_kwargs = {
            "company": company,
            "period": period,
            "date": entry_date,
            "description": description,
            "created_by": getattr(invoice, "created_by", None),
        }
        if hasattr(JournalEntry, "source_key"):
            create_kwargs["source_key"] = f"fiscal_invoice:{invoice.pk}"

        entry = JournalEntry.objects.create(**create_kwargs)

        account_cash = AccountingService.get_account(
            company, "CASH", "account_cash", "Caja"
        )
        account_sales = AccountingService.get_account(
            company, "SALES_GOODS", "account_sales_goods", "Ventas"
        )
        account_tax = AccountingService.get_account(
            company, "IVA_DEBIT", "account_iva_debit", "IVA Débito Fiscal"
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
            description="IVA Débito Fiscal",
        )

        return entry

    @staticmethod
    @transaction.atomic
    def reverse_entry(entry):
        """
        Genera el reverso exacto de un asiento contable.
        """
        company = entry.company
        today = timezone.now().date()
        period = AccountingService.get_period(company, today)

        reverse = JournalEntry.objects.create(
            company=company,
            period=period,
            date=today,
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

@staticmethod
def ensure_required_accounts(company):
    """
    Método de compatibilidad para signals y flujos legacy.
    Evita fallos en la creación automática de empresas.
    """
    return []        