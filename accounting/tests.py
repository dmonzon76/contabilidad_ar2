from decimal import Decimal
from datetime import date
from django.test import TestCase
from unittest.mock import MagicMock

from company.models import Company
from accounting.models import (
    JournalEntry,
    JournalEntryLine,
    Account,
    Period,
    FiscalYear,
)
from accounting.services import AccountingService


class AccountingServiceTestCase(TestCase):

    def setUp(self):
        # 1. Crear empresa de prueba
        self.company = Company.objects.create(
            name="Empresa Test S.A.", tax_id="30-12345678-9"
        )

        # 2. Crear Ejercicio Fiscal (FiscalYear)
        self.fiscal_year, _ = FiscalYear.objects.get_or_create(
            company=self.company,
            year=2026,
            defaults={
                "start_date": date(2026, 1, 1),
                "end_date": date(2026, 12, 31),
            },
        )

        # 3. Crear Período vinculado explícitamente a FiscalYear
        self.period, _ = Period.objects.get_or_create(
            fiscal_year=self.fiscal_year,
            month=1,
            defaults={
                "start_date": date(2026, 1, 1),
                "end_date": date(2026, 1, 31),
                "status": "OPEN",
            },
        )

        # 4. Cuentas contables mínimas requeridas
        accounts = {
            "account_client": ("CLIENTES", "Deudores por Ventas", "ASSET"),
            "account_sales": ("VENTAS", "Ventas de Mercaderías", "INCOME"),
            "account_sales_services": ("VENTAS_SERVICIOS", "Ventas de Servicios", "INCOME"),
            "account_iva_debito": ("IVA_DEBITO", "IVA Débito Fiscal", "LIABILITY"),
            "account_iibb": ("PERCEPCION_IIBB_A_DEPOSITAR", "Percepción IIBB Practicada", "LIABILITY"),
            "account_vat_perc": ("PERCEPCION_IVA_A_DEPOSITAR", "Percepción IVA Practicada", "LIABILITY"),
            "account_cmv": ("CMV", "Costo de Mercaderías Vendidas", "EXPENSE"),
            "account_inventory": ("INVENTARIO", "Mercaderías de Reventa", "ASSET"),
        }

        for attribute, (code, name, account_type) in accounts.items():
            account, _ = Account.objects.get_or_create(
                company=self.company,
                code=code,
                defaults={"name": name, "account_type": account_type},
            )
            setattr(self, attribute, account)

    def test_post_sale_goods_success(self):
        """Prueba la contabilización de venta de mercadería con impuestos y costo."""
        customer_mock = MagicMock()
        customer_mock.name = "Cliente Prueba SRL"

        sale_mock = MagicMock()
        sale_mock.company = self.company
        sale_mock.date = date(2026, 5, 10)
        sale_mock.number = "0001-00000100"
        sale_mock.customer = customer_mock
        sale_mock.total_amount = Decimal("125500.00")
        sale_mock.net_amount = Decimal("100000.00")
        sale_mock.iva_amount = Decimal("21000.00")
        sale_mock.iibb_perception_amount = Decimal("3000.00")
        sale_mock.vat_perception_amount = Decimal("1500.00")
        sale_mock.total_cost = Decimal("60000.00")
        sale_mock.is_service = False
        sale_mock.created_by = None

        entry = AccountingService.post_sale(sale_mock)

        self.assertIsInstance(entry, JournalEntry)
        self.assertEqual(entry.company, self.company)

        # Validar partida doble (Debe == Haber)
        lines = entry.lines.all()
        total_debit = sum(line.debit for line in lines if line.debit)
        total_credit = sum(line.credit for line in lines if line.credit)
        self.assertEqual(total_debit, total_credit)

    def test_post_sale_service_no_inventory_cost(self):
        """Prueba venta de servicio (no debe afectar cuentas de inventario ni CMV)."""
        customer_mock = MagicMock()
        customer_mock.name = "Cliente Servicios S.A."

        sale_mock = MagicMock()
        sale_mock.company = self.company
        sale_mock.date = date(2026, 5, 12)
        sale_mock.number = "0001-00000101"
        sale_mock.customer = customer_mock
        sale_mock.total_amount = Decimal("121000.00")
        sale_mock.net_amount = Decimal("100000.00")
        sale_mock.iva_amount = Decimal("21000.00")
        sale_mock.iibb_perception_amount = Decimal("0.00")
        sale_mock.vat_perception_amount = Decimal("0.00")
        sale_mock.total_cost = Decimal("0.00")
        sale_mock.is_service = True
        sale_mock.created_by = None

        entry = AccountingService.post_sale(sale_mock)

        self.assertFalse(entry.lines.filter(account__code="CMV").exists())
        self.assertFalse(entry.lines.filter(account__code="INVENTARIO").exists())

    def test_post_sale_is_idempotent_for_same_sale(self):
        """No debe crear un segundo asiento para la misma venta al llamarse dos veces."""
        customer_mock = MagicMock()
        customer_mock.name = "Cliente Idempotente"

        sale_mock = MagicMock()
        sale_mock.company = self.company
        sale_mock.date = date(2026, 6, 10)
        sale_mock.number = "0001-00000102"
        sale_mock.customer = customer_mock
        sale_mock.total_amount = Decimal("121000.00")
        sale_mock.net_amount = Decimal("100000.00")
        sale_mock.iva_amount = Decimal("21000.00")
        sale_mock.iibb_perception_amount = Decimal("0.00")
        sale_mock.vat_perception_amount = Decimal("0.00")
        sale_mock.total_cost = Decimal("60000.00")
        sale_mock.is_service = False
        sale_mock.created_by = None

        first = AccountingService.post_sale(sale_mock)
        second = AccountingService.post_sale(sale_mock)

        self.assertEqual(
            JournalEntry.objects.filter(
                company=self.company,
                description=f"Venta {sale_mock.number}",
            ).count(),
            1,
        )
        self.assertEqual(first.pk, second.pk)