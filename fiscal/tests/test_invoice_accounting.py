from datetime import date
from decimal import Decimal

from django.conf.locale import fy
from django.test import TestCase

from accounting.models.journal import JournalEntry
from accounting.models.period import FiscalYear, Period
from company.models import Company
from fiscal.models.fiscal_invoice import FiscalInvoice
from fiscal.models.fiscal_invoice_line import FiscalInvoiceLine


def make_company():
    return Company.objects.create(
        name="Test Co",
        tax_id="30000000001",
        afip_category="RI",
    )


class InvoiceAccountingTests(TestCase):

    def setUp(self):
        self.company = make_company()
        fy, _ = FiscalYear.objects.get_or_create(
        
        company=self.company,
    year=2026,
    defaults={"start_date": date(2026, 1, 1), "end_date": date(2026, 12, 31)},
)
    Period.objects.get_or_create(
    fiscal_year=fy,
    month=9,
    defaults={"start_date": date(2026, 9, 1), "end_date": date(2026, 9, 30), "status": "OPEN"},
)

    def test_invoice_creates_journal_entry(self):
        invoice = FiscalInvoice.objects.create(
            company=self.company,
            point_of_sale=1,
            number=1,
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Producto A",
            quantity=1,
            price=1000,
            vat_rate=Decimal("0.21"),
        )

        invoice.calculate_totals()
        invoice.post_to_accounting()

        entry = JournalEntry.objects.get(company=self.company)
        self.assertTrue(entry.is_balanced)
        self.assertEqual(entry.total_debit, entry.total_credit)
