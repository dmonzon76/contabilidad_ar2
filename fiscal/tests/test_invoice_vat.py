from decimal import Decimal

from django.test import TestCase

from company.models import Company
from accounting.models.tax import Tax
from fiscal.models.fiscal_invoice import FiscalInvoice
from fiscal.models.fiscal_invoice_line import FiscalInvoiceLine


def make_company():
    return Company.objects.create(
        name="Test Co",
        tax_id="30000000001",
        afip_category="RI",
    )


class InvoiceVATTests(TestCase):

    def setUp(self):
        self.company = make_company()

        # Impuestos de IVA con code único
        self.tax_21 = Tax.objects.create(
            code="IVA21",
            name="IVA 21",
            rate=Decimal("21.00"),
            afip_code=5,
            is_vat=True,
        )
        self.tax_105 = Tax.objects.create(
            code="IVA105",
            name="IVA 10.5",
            rate=Decimal("10.50"),
            afip_code=4,
            is_vat=True,
        )
        self.tax_27 = Tax.objects.create(
            code="IVA27",
            name="IVA 27",
            rate=Decimal("27.00"),
            afip_code=6,
            is_vat=True,
        )
        self.tax_exempt = Tax.objects.create(
            code="IVAEX",
            name="IVA Exento",
            rate=Decimal("0.00"),
            afip_code=1,
            is_vat=True,
        )

    def test_vat_21_calculation(self):
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

        self.assertEqual(invoice.vat_amount, Decimal("210"))
        self.assertEqual(invoice.total_amount, Decimal("1210"))

    def test_vat_105_calculation(self):
        invoice = FiscalInvoice.objects.create(
            company=self.company,
            point_of_sale=1,
            number=2,
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Producto B",
            quantity=1,
            price=1000,
            vat_rate=Decimal("0.105"),
        )

        invoice.calculate_totals()

        self.assertEqual(invoice.vat_amount, Decimal("105"))
        self.assertEqual(invoice.total_amount, Decimal("1105"))

    def test_vat_27_calculation(self):
        invoice = FiscalInvoice.objects.create(
            company=self.company,
            point_of_sale=1,
            number=3,
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Producto C",
            quantity=1,
            price=1000,
            vat_rate=Decimal("0.27"),
        )

        invoice.calculate_totals()

        self.assertEqual(invoice.vat_amount, Decimal("270"))
        self.assertEqual(invoice.total_amount, Decimal("1270"))

    def test_multiple_vat_rates(self):
        invoice = FiscalInvoice.objects.create(
            company=self.company,
            point_of_sale=1,
            number=4,
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Prod A",
            quantity=1,
            price=1000,
            vat_rate=Decimal("0.21"),
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Prod B",
            quantity=1,
            price=500,
            vat_rate=Decimal("0.105"),
        )

        invoice.calculate_totals()

        self.assertEqual(invoice.vat_amount, Decimal("262.5"))
        self.assertEqual(invoice.total_amount, Decimal("1762.5"))

    def test_vat_exempt(self):
        invoice = FiscalInvoice.objects.create(
            company=self.company,
            point_of_sale=1,
            number=5,
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Servicio Exento",
            quantity=1,
            price=1000,
            vat_rate=Decimal("0.0"),
        )

        invoice.calculate_totals()

        self.assertEqual(invoice.vat_amount, Decimal("0"))
        self.assertEqual(invoice.total_amount, Decimal("1000"))
