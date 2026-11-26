from datetime import date
from decimal import Decimal

from django.test import TestCase

from accounting.models import (
    Account,
    FiscalYear,
    Period,
)
from company.models import Company
from customers.models import Customer


class BaseSalesTestCase(TestCase):
    def create_company(self):
        return Company.objects.create(
            name="Test Company",
        )

    def create_customer(self, company):
        return Customer.objects.create(
            company=company,
            name="Test Customer",
        )

    def create_open_period(self, company):

        fiscal_year = FiscalYear.objects.create(
            company=company,
            year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="OPEN",
        )

        return Period.objects.create(
            fiscal_year=fiscal_year,
            month=11,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 30),
            status="OPEN",
        )

    def create_minimal_chart(self, company):

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
