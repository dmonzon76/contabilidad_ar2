from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from accounting.models import AccountingSettings
from accounting.models.account import Account
from accounting.models.period import FiscalYear, Period
from accounting.services import AccountingService
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
        self.tax_27, _ = Tax.objects.get_or_create(
            code="IVA_27",
            defaults={
                "name": "IVA 27%",
                "rate": Decimal("27.00"),
                "is_vat": True,
                "afip_code": 6,
            },
        )
        self.tax_non_taxed, _ = Tax.objects.get_or_create(
            code="NO_GRAVADO",
            defaults={
                "name": "No gravado",
                "rate": Decimal("0.00"),
                "is_non_taxed": True,
                "afip_code": 2,
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

    @patch("accounting.services.AccountingService.post_purchase")
    def test_saving_purchase_does_not_post_incomplete_accounting_entry(self, post_purchase):
        Purchase.objects.create(
            company=self.company,
            supplier=self.supplier,
            date=date(2026, 9, 20),
            invoice_number="0001-00001235",
        )

        post_purchase.assert_not_called()

    
    
    def test_post_purchase_records_expenses_and_balances_without_inventory_or_retentions(self):
        expense_account = Account.objects.create(
            company=self.company,
            code="GASTO_PRUEBA",
            name="Gastos de prueba",
            account_type="EXPENSE",
        )
        supplier_account = Account.objects.create(
            company=self.company,
            code="PROVEEDORES_TEST",
            name="Proveedores",
            account_type="LIABILITY",
        )
        vat_account = Account.objects.create(
            company=self.company,
            code="IVA_CREDITO_TEST",
            name="IVA Crédito Fiscal",
            account_type="ASSET",
        )
        perception_account = Account.objects.create(
            company=self.company,
            code="PERCEPCION_TEST",
            name="Percepciones Sufridas",
            account_type="ASSET",
        )
        inventory_account = Account.objects.get(company=self.company, code="INVENTARIO")
        AccountingSettings.objects.create(
            company=self.company,
            account_expenses=expense_account,
            account_inventory=inventory_account,
            account_suppliers=supplier_account,
            account_iva_credit=vat_account,
        )
        purchase = Purchase.objects.create(
            company=self.company,
            supplier=self.supplier,
            date=date(2026, 9, 20),
            invoice_number="0001-00001241",
        )
        PurchaseLine.objects.create(
            purchase=purchase,
            description="Gasto de prueba",
            quantity=Decimal("1.00"),
            unit_price=Decimal("1000.00"),
            tax=self.tax_21,
        )
        PurchasePerception.objects.create(
            purchase=purchase,
            perception_type="IIBB",
            amount=Decimal("300.00"),
            account=perception_account,
        )
        purchase.calculate_totals()

        entry = AccountingService.post_purchase(purchase)

        self.assertEqual(
            entry.lines.get(account=expense_account).debit,
            Decimal("1000.00"),
        )
        self.assertEqual(entry.lines.get(account=vat_account).debit, Decimal("210.00"))
        self.assertEqual(entry.lines.get(account=perception_account).debit, Decimal("300.00"))
        self.assertEqual(entry.lines.get(account=supplier_account).credit, Decimal("1510.00"))
        self.assertFalse(entry.lines.filter(account=inventory_account).exists())
        debits = sum(line.debit for line in entry.lines.all())
        credits = sum(line.credit for line in entry.lines.all())
        self.assertEqual(debits, credits)

    @patch("accounting.services.AccountingService.post_purchase")
    @patch("inventory.integration.update_inventory_from_purchase")
    def test_create_view_persists_purchase_and_tax_formsets(self, update_inventory, post_purchase):
        session = self.client.session
        session["active_company_id"] = self.company.pk
        session.save()

        response = self.client.post(
            reverse("purchases:purchase_create"),
            {
                "supplier": self.supplier.pk,
                "date": "2026-09-20",
                "invoice_number": "0001-00001237",
                "lines-TOTAL_FORMS": "1",
                "lines-INITIAL_FORMS": "0",
                "lines-0-description": "Insumos varios",
                "lines-0-quantity": "10.00",
                "lines-0-unit_price": "1000.00",
                "lines-0-tax": self.tax_21.pk,
                "lines-0-expense_account": "",
                "lines-0-DELETE": "",
                "taxes-TOTAL_FORMS": "1",
                "taxes-INITIAL_FORMS": "0",
                "taxes-0-tax": self.tax_21.pk,
                "taxes-0-taxable_base": "10000.00",
                "taxes-0-DELETE": "",
                "perceptions-TOTAL_FORMS": "2",
                "perceptions-INITIAL_FORMS": "0",
                "perceptions-0-perception_type": "IIBB",
                "perceptions-0-amount": "300.00",
                "perceptions-0-DELETE": "",
                "perceptions-1-perception_type": "IVA",
                "perceptions-1-amount": "175.00",
                "perceptions-1-DELETE": "",
                "retentions-TOTAL_FORMS": "1",
                "retentions-INITIAL_FORMS": "0",
                "retentions-0-retention_type": "GAN",
                "retentions-0-amount": "150.00",
                "retentions-0-DELETE": "",
            },
        )

        self.assertEqual(response.status_code, 302, response.content.decode())
        purchase = Purchase.objects.get(invoice_number="0001-00001237")
        self.assertEqual(purchase.net_amount, Decimal("10000.00"))
        self.assertEqual(purchase.tax_amount, Decimal("2100.00"))
        self.assertEqual(purchase.perception_amount, Decimal("475.00"))
        self.assertEqual(purchase.perceptions.count(), 2)
        self.assertEqual(
            purchase.perceptions.get(perception_type="IVA").amount,
            Decimal("175.00"),
        )
        self.assertEqual(purchase.retention_amount, Decimal("150.00"))
        self.assertEqual(purchase.total_amount, Decimal("12425.00"))
        post_purchase.assert_called_once_with(purchase)
        update_inventory.assert_called_once_with(purchase)

    def test_create_form_shows_tax_rates_and_live_total_fields(self):
        session = self.client.session
        session["active_company_id"] = self.company.pk
        session.save()

        response = self.client.get(reverse("purchases:purchase_create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-rate="21.00"')
        self.assertContains(response, 'id="id_taxes-0-taxable_base"')
        self.assertContains(response, 'id="add-perception"')
        self.assertContains(response, 'id="empty-perception-form"')
        self.assertEqual(response.context["retention_formset"].total_form_count(), 0)
        self.assertContains(response, 'id="add-retention"')
        self.assertContains(response, 'id="purchase-total"')
        self.assertContains(response, 'id="recalculate-totals"')

    @patch("accounting.services.AccountingService.post_purchase")
    @patch("inventory.integration.update_inventory_from_purchase")
    def test_create_purchase_with_mixed_line_taxes_and_perceptions(self, update_inventory, post_purchase):
        session = self.client.session
        session["active_company_id"] = self.company.pk
        session.save()

        response = self.client.post(
            reverse("purchases:purchase_create"),
            {
                "supplier": self.supplier.pk,
                "date": "2026-09-20",
                "invoice_number": "0001-00001239",
                "lines-TOTAL_FORMS": "3",
                "lines-INITIAL_FORMS": "0",
                "lines-0-description": "Concepto gravado al 21%",
                "lines-0-quantity": "1.00",
                "lines-0-unit_price": "1000.00",
                "lines-0-tax": self.tax_21.pk,
                "lines-0-expense_account": "",
                "lines-0-DELETE": "",
                "lines-1-description": "Concepto gravado al 27%",
                "lines-1-quantity": "1.00",
                "lines-1-unit_price": "500.00",
                "lines-1-tax": self.tax_27.pk,
                "lines-1-expense_account": "",
                "lines-1-DELETE": "",
                "lines-2-description": "Concepto no gravado",
                "lines-2-quantity": "1.00",
                "lines-2-unit_price": "200.00",
                "lines-2-tax": self.tax_non_taxed.pk,
                "lines-2-expense_account": "",
                "lines-2-DELETE": "",
                "taxes-TOTAL_FORMS": "1",
                "taxes-INITIAL_FORMS": "0",
                "taxes-0-tax": "",
                "taxes-0-taxable_base": "0.00",
                "taxes-0-DELETE": "",
                "perceptions-TOTAL_FORMS": "2",
                "perceptions-INITIAL_FORMS": "0",
                "perceptions-0-perception_type": "IIBB",
                "perceptions-0-amount": "300.00",
                "perceptions-0-DELETE": "",
                "perceptions-1-perception_type": "IVA",
                "perceptions-1-amount": "175.00",
                "perceptions-1-DELETE": "",
                "retentions-TOTAL_FORMS": "1",
                "retentions-INITIAL_FORMS": "0",
                "retentions-0-retention_type": "",
                "retentions-0-amount": "",
                "retentions-0-DELETE": "",
            },
        )

        self.assertEqual(response.status_code, 302, response.content.decode())
        purchase = Purchase.objects.get(invoice_number="0001-00001239")
        self.assertEqual(purchase.net_amount, Decimal("1700.00"))
        self.assertEqual(purchase.tax_amount, Decimal("345.00"))
        self.assertEqual(purchase.perception_amount, Decimal("475.00"))
        self.assertEqual(purchase.total_amount, Decimal("2520.00"))
        self.assertEqual(purchase.perceptions.count(), 2)
        self.assertFalse(purchase.retentions.exists())
        post_purchase.assert_called_once_with(purchase)
        update_inventory.assert_called_once_with(purchase)

    def test_create_view_displays_invalid_line_errors(self):
        session = self.client.session
        session["active_company_id"] = self.company.pk
        session.save()

        response = self.client.post(
            reverse("purchases:purchase_create"),
            {
                "supplier": self.supplier.pk,
                "date": "2026-09-20",
                "invoice_number": "0001-00001238",
                "lines-TOTAL_FORMS": "1",
                "lines-INITIAL_FORMS": "0",
                "lines-0-description": "",
                "lines-0-quantity": "1.00",
                "lines-0-unit_price": "100.00",
                "lines-0-tax": self.tax_21.pk,
                "lines-0-expense_account": "",
                "taxes-TOTAL_FORMS": "1",
                "taxes-INITIAL_FORMS": "0",
                "taxes-0-tax": "",
                "taxes-0-taxable_base": "0.00",
                "perceptions-TOTAL_FORMS": "1",
                "perceptions-INITIAL_FORMS": "0",
                "perceptions-0-perception_type": "",
                "perceptions-0-amount": "",
                "retentions-TOTAL_FORMS": "1",
                "retentions-INITIAL_FORMS": "0",
                "retentions-0-retention_type": "",
                "retentions-0-amount": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No se pudo guardar la compra")
        self.assertContains(response, "renglones de la compra")
        self.assertContains(response, 'id="id_lines-0-description_error"')
        self.assertFalse(Purchase.objects.filter(invoice_number="0001-00001238").exists())
