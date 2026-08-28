from datetime import date, timedelta
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

    subtotal = 0
    vat_amount = 0
    exempt_amount = 0
    non_taxed_amount = 0

    iva_items = []

    for line in lines:
        total_line = line.line_total()
        tax = line.tax

        if tax.is_vat:
            subtotal += total_line
            vat_amount += total_line * (tax.rate / 100)

            iva_items.append({
                "codigo": tax.afip_code,
                "importe": float(total_line * (tax.rate / 100)),
                "base_imponible": float(total_line),
            })

        elif tax.is_exempt:
            exempt_amount += total_line

        elif tax.is_non_taxed:
            non_taxed_amount += total_line

    total = subtotal + vat_amount + exempt_amount + non_taxed_amount

    self.subtotal = subtotal
    self.vat_amount = vat_amount
    self.exempt_amount = exempt_amount
    self.non_taxed_amount = non_taxed_amount
    self.total = total

    if settings.AFIP_MODE == "testing":
        self.cae = "SIMULATED-CAE-12345678"
        self.cae_due_date = date.today() + timedelta(days=10)

    else:
        wsfe = WSFEClient(
            cert=settings.AFIP_CERT,
            key=settings.AFIP_KEY,
            cuit=self.company.cuit,
        )

        cae_data = wsfe.create_invoice(
            voucher_type=self.voucher_type,
            point_of_sale=self.point_of_sale,
            voucher_number=self.voucher_number,
            total=self.total,
            subtotal=self.subtotal,
            vat_amount=self.vat_amount,
            exempt_amount=self.exempt_amount,
            non_taxed_amount=self.non_taxed_amount,
            customer_cuit=self.customer.cuit,
            date=self.date,
            iva_items=iva_items,   # ← INTEGRACIÓN AFIP
        )

        if not cae_data.success:
            raise ValueError(f"AFIP rejected invoice: {cae_data.error}")

        self.cae = cae_data.cae
        self.cae_due_date = cae_data.due_date

    self.is_closed = True
    self.save()

    return True
