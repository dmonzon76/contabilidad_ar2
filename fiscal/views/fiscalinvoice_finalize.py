from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings
from django.db import transaction

from fiscal.models import FiscalInvoiceLine
from fiscal.afip.wsfe_client import WSFEClient


@transaction.atomic
def finalize(self):
    if self.is_closed:
        raise ValueError("Invoice already finalized")

    lines = FiscalInvoiceLine.objects.filter(invoice=self)
    if not lines.exists():
        raise ValueError("Cannot finalize invoice without lines")

    subtotal = Decimal("0.00")
    vat_amount = Decimal("0.00")
    exempt_amount = Decimal("0.00")
    non_taxed_amount = Decimal("0.00")
    iva_items = []

    for line in lines:
        if line.tax is None:
            continue

        total_line = line.line_total
        tax = line.tax

        if tax.is_vat:
            subtotal += total_line
            tax_value = total_line * (tax.rate / Decimal("100"))
            vat_amount += tax_value

            iva_items.append(
                {
                    "codigo": tax.afip_code,
                    "importe": float(tax_value),
                    "base_imponible": float(total_line),
                }
            )

        elif tax.is_exempt:
            exempt_amount += total_line

        elif tax.is_non_taxed:
            non_taxed_amount += total_line

    total = subtotal + vat_amount + exempt_amount + non_taxed_amount

    self.net_amount = subtotal
    self.tax_amount = vat_amount
    self.total_amount = total
    self.vat_21 = sum(
        (
            line.line_total * (line.tax.rate / Decimal("100"))
            for line in lines
            if line.tax and line.tax.afip_code == 5
        ),
        Decimal("0.00"),
    )
    self.vat_105 = sum(
        (
            line.line_total * (line.tax.rate / Decimal("100"))
            for line in lines
            if line.tax and line.tax.afip_code == 4
        ),
        Decimal("0.00"),
    )
    self.vat_27 = sum(
        (
            line.line_total * (line.tax.rate / Decimal("100"))
            for line in lines
            if line.tax and line.tax.afip_code == 6
        ),
        Decimal("0.00"),
    )
    self.vat_exempt = sum(
        (line.line_total for line in lines if line.tax and line.tax.afip_code == 1),
        Decimal("0.00"),
    )
    self.vat_non_taxed = sum(
        (line.line_total for line in lines if line.tax and line.tax.afip_code == 2),
        Decimal("0.00"),
    )

    if settings.AFIP_MODE == "testing":
        self.cae = f"SIM-{self.voucher_book.point_of_sale}-{self.voucher_book.voucher_type}-{self.number or 1}"
        self.cae_due_date = date.today() + timedelta(days=10)
    else:
        wsfe = WSFEClient(
            cert=settings.AFIP_CERT,
            key=settings.AFIP_KEY,
            cuit=self.company.cuit,
        )

        cae_data = wsfe.create_invoice(
            voucher_type=self.voucher_book.voucher_type,
            point_of_sale=self.voucher_book.point_of_sale,
            voucher_number=self.number,
            total=float(total),
            subtotal=float(subtotal),
            vat_amount=float(vat_amount),
            exempt_amount=float(exempt_amount),
            non_taxed_amount=float(non_taxed_amount),
            customer_cuit=self.customer_tax_id or "0",
            date=self.date,
        )

        if not cae_data.success:
            raise ValueError(f"AFIP rejected invoice: {cae_data.error}")

        self.cae = cae_data.cae
        self.cae_due_date = cae_data.due_date

    self.is_closed = True
    self.save()
    return True
