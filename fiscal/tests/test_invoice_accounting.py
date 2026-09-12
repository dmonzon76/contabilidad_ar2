from decimal import Decimal

from django.test import TestCase

from company.models import Company
from accounting.models.journal import JournalEntry, JournalEntryLine
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
