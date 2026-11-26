from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError

import accounting.models
import inventory.integration
from accounting.models import (
    Account,
    FiscalYear,
    Period,
)
from accounting.services import AccountingService
from company.models import Company
from customers.models import Customer
from inventory.models import InventoryItem, InventoryMovement, Location
from products.models import Product
from sales.models.sale import Sale
from sales.models.sale_item import SaleItem
from sales.tests.base import BaseSalesTestCase


class InventoryValidationTests(BaseSalesTestCase):
    def test_cannot_issue_sale_without_inventory_item(self):
        """
        Una venta con producto físico debe bloquearse
        cuando no existe InventoryItem.
        """

        company = self.create_company()

        customer = self.create_customer(company)

        product = Product.objects.create(
            company=company,
            name="Test Product",
            sku="TEST001",
            type="PRODUCT",
            price=Decimal("100.00"),
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

        with self.assertRaises(ValidationError):
            inventory.integration.validate_inventory_before_issue(sale)

    def test_post_sale_creates_journal_entry(self):
        """
        Una venta contabilizada debe generar un JournalEntry.
        """

        company = Company.objects.create(
            name="Test Company",
        )

        customer = Customer.objects.create(
            company=company,
            name="Test Customer",
        )

        fiscal_year = accounting.models.FiscalYear.objects.create(
            company=company,
            year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="OPEN",
        )

        accounting.models.Period.objects.create(
            fiscal_year=fiscal_year,
            month=11,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 30),
            status="OPEN",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="1",
            name="Assets",
            account_type="ASSET",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="1.1",
            name="Current Assets",
            account_type="ASSET",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="1.1.04",
            name="Accounts Receivable",
            account_type="ASSET",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="4",
            name="Revenue",
            account_type="INCOME",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="4.1",
            name="Sales",
            account_type="INCOME",
        )

        accounting.models.Account.objects.create(
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
            accounting.models.JournalEntry.objects.filter(
                source_key=f"sale:{sale.pk}"
            ).count(),
            1,
        )

    def test_issue_sale_creates_inventory_movement(self):
        """
        Una venta válida debe generar un InventoryMovement.
        """

        company = Company.objects.create(
            name="Test Company",
        )

        customer = Customer.objects.create(
            company=company,
            name="Test Customer",
        )

        product = Product.objects.create(
            company=company,
            name="Test Product",
            sku="TEST002",
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

        self.assertEqual(
            InventoryMovement.objects.filter(
                sale=sale
            ).count(),
            1,
        ) 

    def test_post_sale_creates_customer_ledger(self):
        """
        Una venta contabilizada debe generar un movimiento
        de cuenta corriente del cliente.
        """

        company = Company.objects.create(
            name="Test Company",
        )

        customer = Customer.objects.create(
            company=company,
            name="Test Customer",
        )

        fiscal_year = accounting.models.FiscalYear.objects.create(
            company=company,
            year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="OPEN",
        )

        accounting.models.Period.objects.create(
            fiscal_year=fiscal_year,
            month=11,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 30),
            status="OPEN",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="1",
            name="Assets",
            account_type="ASSET",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="1.1",
            name="Current Assets",
            account_type="ASSET",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="1.1.04",
            name="Accounts Receivable",
            account_type="ASSET",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="4",
            name="Revenue",
            account_type="INCOME",
        )

        accounting.models.Account.objects.create(
            company=company,
            code="4.1",
            name="Sales",
            account_type="INCOME",
        )

        accounting.models.Account.objects.create(
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
            accounting.models.AccountMovement.objects.filter(
                sale=sale
            ).count(),
            1,
        )

    def test_post_sale_does_not_duplicate_customer_ledger(self):
        """
        La contabilización repetida no debe duplicar
        movimientos de cuenta corriente.
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
        AccountingService.post_sale(sale)

        self.assertEqual(
            accounting.models.AccountMovement.objects.filter(
                sale=sale
            ).count(),
            1,
        )    

