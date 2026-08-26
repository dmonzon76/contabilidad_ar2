from datetime import date, timedelta
from django.conf import settings
from django.db import transaction


from fiscal.models import FiscalInvoiceLine
from fiscal.afip.wsfe_client import WSFEClient

@transaction.atomic
def finalize(self):
    """
    Finaliza la factura fiscal:
    - Calcula totales
    - Valida integridad
    - Solicita CAE (testing o producción)
    - Cierra la factura
    """

    if self.is_closed:
        raise ValueError("Invoice already finalized")

    # 1) Validar que existan líneas
    lines = FiscalInvoiceLine.objects.filter(invoice=self)
    if not lines.exists():
        raise ValueError("Cannot finalize invoice without lines")

    # 2) Calcular totales
    subtotal = 0
    vat_amount = 0
    exempt_amount = 0
    non_taxed_amount = 0

    for line in lines:
        line_total = line.quantity * line.unit_price

        if line.vat_rate > 0:
            subtotal += line_total
            vat_amount += line_total * (line.vat_rate / 100)
        elif line.is_exempt:
            exempt_amount += line_total
        else:
            non_taxed_amount += line_total

    total = subtotal + vat_amount + exempt_amount + non_taxed_amount

    # Guardar totales
    self.subtotal = subtotal
    self.vat_amount = vat_amount
    self.exempt_amount = exempt_amount
    self.non_taxed_amount = non_taxed_amount
    self.total = total

    # 3) Solicitar CAE
    if settings.AFIP_MODE == "testing":
        self.cae = "SIMULATED-CAE-12345678"
        self.cae_due_date = date.today() + timedelta(days=10)

    else:
        # Producción: llamar WSFE real
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
        )

        if not cae_data.success:
            raise ValueError(f"AFIP rejected invoice: {cae_data.error}")

        self.cae = cae_data.cae
        self.cae_due_date = cae_data.due_date

    # 4) Cerrar factura
    self.is_closed = True
    self.save()

    return True



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
)
