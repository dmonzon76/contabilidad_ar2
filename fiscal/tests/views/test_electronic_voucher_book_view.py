from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from company.models import Company, UserCompany
from fiscal.models.fiscal_invoice import FiscalInvoice
from fiscal.models.fiscal_invoice_line import FiscalInvoiceLine
from fiscal.models.vat_book import VATBookEntry


def make_company(name):
    return Company.objects.create(
        name=name,
        tax_id="30000000001",
        afip_category="RI",
    )


class ElectronicVoucherBookViewTests(TestCase):

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

        # Factura finalizada con libro IVA
        invoice = FiscalInvoice.objects.create(
            company=self.company_a,
            point_of_sale=1,
            number=1,
            cae="11112222",
            cae_due_date="2026-12-31",
            is_finalized=True,
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Producto A",
            quantity=1,
            price=1000,
            vat_rate=0.21,
        )

        VATBookEntry.objects.create(
            invoice=invoice,
            company=self.company_a,
            taxable_amount=1000,
            vat_amount=210,
            total_amount=1210,
            point_of_sale=1,
            number=1,
        )

    def test_requires_login(self):
        response = self.client.get(reverse("fiscal:voucher_book"))
        self.assertEqual(response.status_code, 302)

    def test_denies_access_to_other_company(self):
        self.client.login(username="daniel", password="123")

        session = self.client.session
        session["active_company_id"] = self.company_b.id
        session.save()

        with self.assertRaises(PermissionDenied):
            self.client.get(reverse("fiscal:voucher_book"))

    def test_loads_vat_book_entries_correctly(self):
        self.client.login(username="daniel", password="123")

        session = self.client.session
        session["active_company_id"] = self.company_a.id
        session.save()

        response = self.client.get(reverse("fiscal:voucher_book"))
        self.assertEqual(response.status_code, 200)

        # Datos del libro IVA
        self.assertContains(response, "1000")   # base imponible
        self.assertContains(response, "210")    # IVA
        self.assertContains(response, "1210")   # total
        self.assertContains(response, "11112222")  # CAE
        self.assertContains(response, "1")      # punto de venta / número
