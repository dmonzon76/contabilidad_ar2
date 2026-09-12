from django.test import TestCase
from unittest.mock import patch

from company.models import Company
from fiscal.models.fiscal_invoice import FiscalInvoice
from fiscal.models.electronic_voucher_book import ElectronicVoucherBook


def make_company():
    return Company.objects.create(
        name="Test Co",
        tax_id="30000000001",
        afip_category="RI",
    )


class InvoiceNumberingTests(TestCase):

    def setUp(self):
        self.company = make_company()
        self.book = ElectronicVoucherBook.objects.create(
            company=self.company,
            point_of_sale=1,
            voucher_type="A",
            enabled=True,
            current_number=0,
        )

    def test_local_numbering_is_correlative(self):
        inv1 = FiscalInvoice.objects.create(
            company=self.company,
            voucher_book=self.book,
            number=1,
            date="2026-01-01",
            customer_name="Test",
        )
        inv2 = FiscalInvoice.objects.create(
            company=self.company,
            voucher_book=self.book,
            number=2,
            date="2026-01-02",
            customer_name="Test",
        )

        self.assertEqual(inv1.number, 1)
        self.assertEqual(inv2.number, 2)

    def test_duplicate_number_is_not_allowed(self):
        FiscalInvoice.objects.create(
            company=self.company,
            voucher_book=self.book,
            number=1,
            date="2026-01-01",
            customer_name="Test",
        )

        with self.assertRaises(Exception):
            FiscalInvoice.objects.create(
                company=self.company,
                voucher_book=self.book,
                number=1,
                date="2026-01-02",
                customer_name="Test",
            )

    @patch("fiscal.afip.wsfe_client.WSFEClient.get_last_authorized",
           return_value={"number": 150, "point_of_sale": 1})
    def test_local_number_matches_afip(self, mock_last):
        from fiscal.models.fiscal_invoice import FiscalInvoice

        afip_data = FiscalInvoice.next_number(
            company=self.company,
            point_of_sale=1,
            voucher_type="A",
        )

        invoice = FiscalInvoice.objects.create(
            company=self.company,
            voucher_book=self.book,
            number=afip_data,
            date="2026-01-01",
            customer_name="Test",
        )

        self.assertEqual(invoice.number, 151)
