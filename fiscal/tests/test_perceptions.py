from decimal import Decimal

from django.test import TestCase

from company.models import Company
from fiscal.models.fiscal_invoice import FiscalInvoice
from fiscal.models.fiscal_invoice_line import FiscalInvoiceLine
from fiscal.utils.perceptions import (
    calculate_iibb_perception,
    calculate_iva_perception,
    calculate_rg4815_perception,
)


def make_company():
    return Company.objects.create(
        name="Test Co",
        tax_id="30000000001",
        afip_category="RI",
    )


class PerceptionsTests(TestCase):

    def setUp(self):
        self.company = make_company()

    def test_iibb_perception(self):
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

        result = calculate_iibb_perception(invoice)
        self.assertAlmostEqual(result, 35.0)  # 3.5% AGIP

    def test_iva_perception(self):
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
            vat_rate=Decimal("0.21"),
        )

        result = calculate_iva_perception(invoice)
        self.assertAlmostEqual(result, 50.0)  # 5% percepción IVA

    def test_rg4815_perception(self):
        invoice = FiscalInvoice.objects.create(
            company=self.company,
            point_of_sale=1,
            number=3,
        )

        FiscalInvoiceLine.objects.create(
            invoice=invoice,
            description="Servicio Digital",
            quantity=1,
            price=1000,
            vat_rate=Decimal("0.21"),
        )

        result = calculate_rg4815_perception(invoice)
        self.assertAlmostEqual(result, 450.0)  # 45% RG 4815
