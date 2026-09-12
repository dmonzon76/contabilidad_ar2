from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from django.core.exceptions import PermissionDenied

from company.models import Company, UserCompany
from fiscal.models.fiscal_invoice import FiscalInvoice
from fiscal.models.fiscal_invoice_line import FiscalInvoiceLine
from accounting.models.journal_entry import JournalEntry
from fiscal.models.vat_book import VATBookEntry


def make_company(name):
    return Company.objects.create(
        name=name,
        tax_id="30000000001",
        afip_category="RI",
    )


class InvoiceFinalizeViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="daniel", password="123")
        self.company_a = make_company("Company A")
        self.company_b = make_company("Company B")

        UserCompany.objects.create(
            user=self.user,
            company=self.company_a,
            is_active=True,
            is_default=True,
        )

        # Factura preliminar
        self.invoice = FiscalInvoice.objects.create(
            company=self.company_a,
            point_of_sale=1,
            number=1,
        )

        FiscalInvoiceLine.objects.create(
            invoice=self.invoice,
            description="Producto A",
            quantity=1,
            price=1000,
            vat_rate=0.21,
        )

    def test_requires_login(self):
        response = self.client.get(reverse("fiscal:invoice_finalize", args=[self.invoice.id]))
        self.assertEqual(response.status_code, 302)

    def test_denies_access_to_other_company(self):
        self.client.login(username="daniel", password="123")

        session = self.client.session
        session["active_company_id"] = self.company_b.id
        session.save()

        with self.assertRaises(PermissionDenied):
            self.client.get(reverse("fiscal:invoice_finalize", args=[self.invoice.id]))

    @patch("fiscal.afip.wsfe_client.WSFEClient.create_invoice",
           return_value={"success": True, "cae": "11112222", "due_date": "2026-12-31"})
    def test_finalize_generates_cae_and_accounting(self, mock_afip):
        self.client.login(username="daniel", password="123")

        session = self.client.session
        session["active_company_id"] = self.company_a.id
        session.save()

        response = self.client.get(reverse("fiscal:invoice_finalize", args=[self.invoice.id]))
        self.assertEqual(response.status_code, 200)

        # CAE guardado
        invoice = FiscalInvoice.objects.get(id=self.invoice.id)
        self.assertEqual(invoice.cae, "11112222")
        self.assertEqual(invoice.cae_due_date, "2026-12-31")
        self.assertTrue(invoice.is_finalized)

        # Asiento contable generado
        entry = JournalEntry.objects.get(invoice=invoice)
        self.assertIsNotNone(entry)

        # Libro IVA generado
        vat_entry = VATBookEntry.objects.get(invoice=invoice)
        self.assertEqual(vat_entry.vat_amount, 210)
        self.assertEqual(vat_entry.taxable_amount, 1000)
        self.assertEqual(vat_entry.total_amount, 1210)
