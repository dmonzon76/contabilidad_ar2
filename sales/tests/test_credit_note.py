from datetime import date
from decimal import Decimal

import inventory.integration
from accounting.models import (
    Account,
    AccountMovement,
    FiscalYear,
    JournalEntry,
    Period,
)
from accounting.services import AccountingService
from company.models import Company
from customers.models import Customer
from inventory.models import (
    InventoryItem,
    InventoryMovement,
    Location,
)
from products.models import Product
from sales.models import CreditNote
from sales.models.sale import Sale
from sales.models.sale_item import SaleItem
from sales.services.credit_note_service import CreditNoteService
from sales.tests.base import BaseSalesTestCase


class CreditNoteTests(BaseSalesTestCase):
    def test_credit_note_creates_credit_customer_ledger(self):
        """
        Una Nota de Crédito emitida debe generar
        un crédito en la cuenta corriente del cliente.
        """

        company = Company.objects.create(
            name="Test Company",
        )

        customer = Customer.objects.create(
            company=company,
            name="Test Customer",
        )

        fiscal_year = FiscalYear.objects.create(
            company=company,
            year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="OPEN",
        )

        Period.objects.create(
            fiscal_year=fiscal_year,
            month=11,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 30),
            status="OPEN",
        )

        Account.objects.create(
            company=company,
            code="1",
            name="Assets",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="1.1",
            name="Current Assets",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="1.1.04",
            name="Accounts Receivable",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="4",
            name="Revenue",
            account_type="INCOME",
        )

        Account.objects.create(
            company=company,
            code="4.1",
            name="Sales",
            account_type="INCOME",
        )

        Account.objects.create(
            company=company,
            code="4.1.01",
            name="Product Sales",
            account_type="INCOME",
        )

        sale = Sale.objects.create(
            company=company,
            customer=customer,
        )

        sale.total_amount = Decimal("1000")
        sale.save()

        AccountingService.post_sale(sale)

        credit_note = CreditNote.objects.create(
            company=company,
            sale=sale,
            customer=customer,
            reason="Test credit note",
            total_amount=sale.total_amount,
        )

        CreditNoteService.issue_credit_note(credit_note)

        self.assertEqual(
            AccountMovement.objects.filter(
                customer=customer,
                movement_type="CREDIT",
            ).count(),
            1,
        )


    def test_credit_note_reverses_inventory(self):
        """
        Una Nota de Crédito debe generar
        una entrada de inventario.
        """

        company = self.create_company()

        customer = self.create_customer(company)

        product = Product.objects.create(
            company=company,
            name="Test Product",
            sku="PROD001",
            type="PRODUCT",
            price=Decimal("100.00"),
        )

        location = Location.objects.create(
            company=company,
            code="MAIN",
            name="Main Warehouse",
        )

        InventoryItem.objects.create(
            company=company,
            product=product,
            location=location,
            quantity=Decimal("100"),
            min_stock=Decimal("0"),
        )

        sale = Sale.objects.create(
            company=company,
            customer=customer,
        )

        SaleItem.objects.create(
            sale=sale,
            product=product,
            description="Test Product",
            quantity=Decimal("5"),
            unit_price=Decimal("100"),
        )

        inventory.integration.validate_inventory_before_issue(sale)

        inventory.integration.update_inventory_from_sale(sale)

        credit_note = CreditNote.objects.create(
            company=company,
            sale=sale,
            customer=customer,
            reason="Inventory return",
            total_amount=Decimal("500"),
        )

        CreditNoteService.issue_credit_note(credit_note)

        self.assertEqual(
            InventoryMovement.objects.filter(movement_type="IN").count(),
            1,
        )

    def test_credit_note_marks_document_as_issued(self):
        """
        La emisión debe cambiar el estado
        de DRAFT a ISSUED.
        """

        company = self.create_company()

        customer = self.create_customer(company)

        sale = Sale.objects.create(
            company=company,
            customer=customer,
        )

        credit_note = CreditNote.objects.create(
            company=company,
            sale=sale,
            customer=customer,
            reason="Issue test",
            total_amount=Decimal("100"),
        )

        self.assertEqual(
            credit_note.status,
            "DRAFT",
        )

        CreditNoteService.issue_credit_note(credit_note)

        credit_note.refresh_from_db()

        self.assertEqual(
            credit_note.status,
            "ISSUED",
        )

    def test_credit_note_creates_reverse_journal_entry(self):
        """
        Una Nota de Crédito debe generar
        un asiento contable inverso al de la venta.
        """

        company = Company.objects.create(
            name="Test Company",
        )

        customer = Customer.objects.create(
            company=company,
            name="Test Customer",
        )

        fiscal_year = FiscalYear.objects.create(
            company=company,
            year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="OPEN",
        )

        Period.objects.create(
            fiscal_year=fiscal_year,
            month=11,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 30),
            status="OPEN",
        )

        Account.objects.create(
            company=company,
            code="1",
            name="Assets",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="1.1",
            name="Current Assets",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="1.1.04",
            name="Accounts Receivable",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="4",
            name="Revenue",
            account_type="INCOME",
        )

        Account.objects.create(
            company=company,
            code="4.1",
            name="Sales",
            account_type="INCOME",
        )

        Account.objects.create(
            company=company,
            code="4.1.01",
            name="Product Sales",
            account_type="INCOME",
        )

        sale = Sale.objects.create(
            company=company,
            customer=customer,
        )

        sale.total_amount = Decimal("1000")
        sale.save()

        AccountingService.post_sale(sale)

        self.assertEqual(
            JournalEntry.objects.count(),
            1,
        )

        credit_note = CreditNote.objects.create(
            company=company,
            sale=sale,
            customer=customer,
            reason="Reverse accounting entry",
            total_amount=sale.total_amount,
        )

        CreditNoteService.issue_credit_note(
            credit_note
        )

        self.assertEqual(
            JournalEntry.objects.count(),
            2,
        )    
    def test_credit_note_does_not_duplicate_reversal(self):
        """
        Emitir dos veces la misma Nota de Crédito
        no debe duplicar movimientos ni asientos.
        """

        company = Company.objects.create(
            name="Test Company",
        )

        customer = Customer.objects.create(
            company=company,
            name="Test Customer",
        )

        fiscal_year = FiscalYear.objects.create(
            company=company,
            year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="OPEN",
        )

        Period.objects.create(
            fiscal_year=fiscal_year,
            month=11,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 30),
            status="OPEN",
        )

        Account.objects.create(
            company=company,
            code="1",
            name="Assets",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="1.1",
            name="Current Assets",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="1.1.04",
            name="Accounts Receivable",
            account_type="ASSET",
        )

        Account.objects.create(
            company=company,
            code="4",
            name="Revenue",
            account_type="INCOME",
        )

        Account.objects.create(
            company=company,
            code="4.1",
            name="Sales",
            account_type="INCOME",
        )

        Account.objects.create(
            company=company,
            code="4.1.01",
            name="Product Sales",
            account_type="INCOME",
        )

        product = Product.objects.create(
            company=company,
            name="Test Product",
            sku="PROD002",
            type="PRODUCT",
            price=Decimal("100.00"),
        )

        location = Location.objects.create(
            company=company,
            code="MAIN",
            name="Main Warehouse",
        )

        InventoryItem.objects.create(
            company=company,
            product=product,
            location=location,
            quantity=Decimal("100"),
            min_stock=Decimal("0"),
        )

        sale = Sale.objects.create(
            company=company,
            customer=customer,
        )

        SaleItem.objects.create(
            sale=sale,
            product=product,
            description="Test Product",
            quantity=Decimal("5"),
            unit_price=Decimal("100"),
        )

        inventory.integration.validate_inventory_before_issue(
            sale
        )

        inventory.integration.update_inventory_from_sale(
            sale
        )

        sale.total_amount = Decimal("500")
        sale.save()

        AccountingService.post_sale(
            sale
        )

        credit_note = CreditNote.objects.create(
            company=company,
            sale=sale,
            customer=customer,
            reason="Duplicate protection",
            total_amount=sale.total_amount,
        )

        CreditNoteService.issue_credit_note(
            credit_note
        )

        CreditNoteService.issue_credit_note(
            credit_note
        )

        self.assertEqual(
            AccountMovement.objects.filter(
                customer=customer,
                movement_type="CREDIT",
            ).count(),
            1,
        )

        self.assertEqual(
            InventoryMovement.objects.filter(
                movement_type="IN",
            ).count(),
            1,
        )

        self.assertEqual(
            JournalEntry.objects.count(),
            2,
        )    