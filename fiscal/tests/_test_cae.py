import pytest
from datetime import date
from unittest.mock import patch

from fiscal.models import FiscalInvoice, FiscalInvoiceLine
from fiscal.afip.wsfe_client import CAEResponse
from sales.models import Sale
from company.models import Company
from customers.models import Customer


# -----------------------------
# CAE SIMULADO (AFIP_MODE = testing)
# -----------------------------
@pytest.mark.django_db
def test_finalize_generates_simulated_cae(settings):
    settings.AFIP_MODE = "testing"

    company = Company.objects.create(name="Test SA", cuit="30-12345678-9")
    customer = Customer.objects.create(name="Cliente", cuit="20-11111111-1")
    sale = Sale.objects.create(company=company, customer=customer, total_cost=100)

    invoice = FiscalInvoice.objects.create(
        company=company,
        customer=customer,
        sale=sale,
        voucher_type="B",
        point_of_sale=1,
        voucher_number=1,
    )

    FiscalInvoiceLine.objects.create(
        invoice=invoice,
        company=company,
        quantity=2,
        unit_price=100,
        vat_rate=21,
    )

    invoice.finalize()

    assert invoice.is_closed is True
    assert invoice.cae.startswith("SIM-")
    assert invoice.total > 0
    assert invoice.vat_amount > 0


# -----------------------------
# CAE REAL MOCKEADO (AFIP_MODE = production)
# -----------------------------
@pytest.mark.django_db
def test_finalize_real_cae_mocked(settings):
    settings.AFIP_MODE = "production"

    company = Company.objects.create(name="Test SA", cuit="30-12345678-9")
    customer = Customer.objects.create(name="Cliente", cuit="20-11111111-1")
    sale = Sale.objects.create(company=company, customer=customer, total_cost=100)

    invoice = FiscalInvoice.objects.create(
        company=company,
        customer=customer,
        sale=sale,
        voucher_type="B",
        point_of_sale=1,
        voucher_number=1,
    )

    FiscalInvoiceLine.objects.create(
        invoice=invoice,
        company=company,
        quantity=1,
        unit_price=100,
        vat_rate=21,
    )

    with patch("fiscal.afip.wsfe_client.WSFEClient.create_invoice") as mock_cae:
        mock_cae.return_value = CAEResponse(
            success=True,
            cae="123456789",
            due_date=date.today(),
        )

        invoice.finalize()

    assert invoice.cae == "123456789"
    assert invoice.is_closed is True


# -----------------------------
# AFIP RECHAZA EL COMPROBANTE
# -----------------------------
@pytest.mark.django_db
def test_finalize_afip_rejects_invoice(settings):
    settings.AFIP_MODE = "production"

    company = Company.objects.create(name="Test SA", cuit="30-12345678-9")
    customer = Customer.objects.create(name="Cliente", cuit="20-11111111-1")
    sale = Sale.objects.create(company=company, customer=customer, total_cost=100)

    invoice = FiscalInvoice.objects.create(
        company=company,
        customer=customer,
        sale=sale,
        voucher_type="B",
        point_of_sale=1,
        voucher_number=1,
    )

    FiscalInvoiceLine.objects.create(
        invoice=invoice,
        company=company,
        quantity=1,
        unit_price=100,
        vat_rate=21,
    )

    with patch("fiscal.afip.wsfe_client.WSFEClient.create_invoice") as mock_cae:
        mock_cae.return_value = CAEResponse(
            success=False,
            error="Rejected by AFIP",
        )

        with pytest.raises(ValueError):
            invoice.finalize()

    assert invoice.is_closed is False
    assert invoice.cae is None


# -----------------------------
# NO SE PUEDE FINALIZAR SIN LÍNEAS
# -----------------------------
@pytest.mark.django_db
def test_finalize_without_lines_fails(settings):
    settings.AFIP_MODE = "testing"

    company = Company.objects.create(name="Test SA", cuit="30-12345678-9")
    customer = Customer.objects.create(name="Cliente", cuit="20-11111111-1")
    sale = Sale.objects.create(company=company, customer=customer, total_cost=100)

    invoice = FiscalInvoice.objects.create(
        company=company,
        customer=customer,
        sale=sale,
        voucher_type="B",
        point_of_sale=1,
        voucher_number=1,
    )

    with pytest.raises(ValueError):
        invoice.finalize()


# -----------------------------
# TOTALES CORRECTOS
# -----------------------------
@pytest.mark.django_db
def test_finalize_totals(settings):
    settings.AFIP_MODE = "testing"

    company = Company.objects.create(name="Test SA", cuit="30-12345678-9")
    customer = Customer.objects.create(name="Cliente", cuit="20-11111111-1")
    sale = Sale.objects.create(company=company, customer=customer, total_cost=100)

    invoice = FiscalInvoice.objects.create(
        company=company,
        customer=customer,
        sale=sale,
        voucher_type="B",
        point_of_sale=1,
        voucher_number=1,
    )

    FiscalInvoiceLine.objects.create(
        invoice=invoice,
        company=company,
        quantity=2,
        unit_price=100,
        vat_rate=21,
    )

    invoice.finalize()

    assert invoice.subtotal == 200
    assert invoice.vat_amount == pytest.approx(42)
    assert invoice.total == pytest.approx(242)
