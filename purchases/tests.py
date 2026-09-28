from datetime import date
from decimal import Decimal

from django.test import TestCase

from accounting.models.account import Account
from accounting.models.period import FiscalYear, Period
from company.models import Company
from fiscal.models import Tax
from purchases.models import Purchase, PurchaseLine, PurchasePerception, PurchaseRetention
from suppliers.models import Supplier


class PurchaseModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Empresa Test S.A.", tax_id="30-11111111-9")
        self.supplier = Supplier.objects.create(company=self.company, name="Proveedor Test SRL", tax_id="30-22222222-9")
        fiscal_year, _ = FiscalYear.objects.get_or_create(
            company=self.company,
            year=2026,
            defaults={
                "start_date": date(2026, 1, 1),
                "end_date": date(2026, 12, 31),
            },
        )
        Period.objects.get_or_create(
            fiscal_year=fiscal_year,
            month=9,
            defaults={
                "start_date": date(2026, 9, 1),
                "end_date": date(2026, 9, 30),
                "status": "OPEN",
            },
        )
        Account.objects.create(
            company=self.company,
            code="INVENTARIO",
            name="Inventario",
            account_type="ASSET",
        )
        Account.objects.create(
            company=self.company,
            code="PROVEEDORES",
            name="Proveedores",
            account_type="LIABILITY",
        )
        self.tax_21, _ = Tax.objects.get_or_create(
            code="IVA_21",
            defaults={
                "name": "IVA 21%",
                "rate": Decimal("21.00"),
                "is_vat": True,
                "afip_code": 5,
            },
        )

    def test_calculate_totals_with_perceptions_and_retentions(self):
        """Verifica el cálculo de totales con renglones, percepciones y retenciones."""
        purchase = Purchase.objects.create(
            company=self.company, supplier=self.supplier, date=date(2026, 9, 20), invoice_number="0001-00001234"
        )

        # Renglón: 10 unidades x $1000 = $10.000 neto + $2.100 IVA
        PurchaseLine.objects.create(
            purchase=purchase,
            description="Insumos varios",
            quantity=Decimal("10.00"),
            unit_price=Decimal("1000.00"),
            tax=self.tax_21,
        )

        # Percepción IIBB ARBA $300
        PurchasePerception.objects.create(
            purchase=purchase, perception_type="IIBB", jurisdiction="ARBA", amount=Decimal("300.00")
        )

        # Retención Ganancias $150
        PurchaseRetention.objects.create(purchase=purchase, retention_type="GAN", amount=Decimal("150.00"))

        purchase.calculate_totals()

        self.assertEqual(purchase.net_amount, Decimal("10000.00"))
        self.assertEqual(purchase.tax_amount, Decimal("2100.00"))
        self.assertEqual(purchase.perception_amount, Decimal("300.00"))
        self.assertEqual(purchase.retention_amount, Decimal("150.00"))

        # Total = 10000 + 2100 + 300 - 150 = 12250
        self.assertEqual(purchase.total_amount, Decimal("12250.00"))
