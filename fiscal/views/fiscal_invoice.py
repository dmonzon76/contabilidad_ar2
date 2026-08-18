from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from fiscal.models.fiscal_invoice import FiscalInvoice
from sales.models.sale import Sale

from accounting.models.journal import JournalEntry, JournalEntryLine
from accounting.models.account import Account
from accounting.models.period import Period

from datetime import date


def get_account(code):
    """Obtiene la cuenta contable por código."""
    return Account.objects.get(code=code)


def current_period(company):
    """Obtiene el período contable activo."""
    return Period.objects.get_current(company=company)


@login_required
def fiscal_invoice_create(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    # Si ya existe factura fiscal, no permitir duplicar
    if hasattr(sale, "fiscal_invoice"):
        return redirect("sales:sale_detail", pk=sale.id)

    if request.method == "POST":

        # Tipo de comprobante y punto de venta (pueden venir de configuración)
        voucher_type = "B"
        point_of_sale = 1

        # Número fiscal correlativo
        voucher_number = FiscalInvoice.next_number(
            company=sale.company,
            point_of_sale=point_of_sale,
            voucher_type=voucher_type
        )

        # Crear factura fiscal
        invoice = FiscalInvoice.objects.create(
            company=sale.company,
            customer=sale.customer,
            sale=sale,
            voucher_type=voucher_type,
            point_of_sale=point_of_sale,
            voucher_number=voucher_number,
        )

        # Calcular totales y generar CAE
        invoice.finalize()

        # Generar asiento contable automático
        generate_accounting_entry(invoice, request.user)

        return redirect("sales:sale_detail", pk=sale.id)

    return render(request, "fiscal/fiscal_invoice_confirm.html", {"sale": sale})

def generate_accounting_entry(invoice, user):
    sale = invoice.sale
    company = sale.company
    period = current_period(company)

    entry = JournalEntry.objects.create(
        company=company,
        period=period,
        date=invoice.date,
        description=f"Fiscal sale {invoice.voucher_number}",
        created_by=user,
    )

    # Caja (contado)
    JournalEntryLine.objects.create(
        entry=entry,
        account=get_account("CAJA"),
        debit=invoice.total,
        description="Cobro de venta fiscal"
    )

    # Ventas
    JournalEntryLine.objects.create(
        entry=entry,
        account=get_account("VENTAS"),
        credit=invoice.subtotal,
        description="Venta fiscal gravada"
    )

    # IVA Débito Fiscal
    if invoice.vat_amount > 0:
        JournalEntryLine.objects.create(
            entry=entry,
            account=get_account("IVA_DEBITO"),
            credit=invoice.vat_amount,
            description="IVA Débito Fiscal"
        )

    # Exento
    if invoice.exempt_amount > 0:
        JournalEntryLine.objects.create(
            entry=entry,
            account=get_account("VENTAS_EXENTAS"),
            credit=invoice.exempt_amount,
            description="Venta exenta"
        )

    # No gravado
    if invoice.non_taxed_amount > 0:
        JournalEntryLine.objects.create(
            entry=entry,
            account=get_account("VENTAS_NO_GRAVADAS"),
            credit=invoice.non_taxed_amount,
            description="Venta no gravada"
        )

    # CMV
    if sale.total_cost > 0:
        JournalEntryLine.objects.create(
            entry=entry,
            account=get_account("CMV"),
            debit=sale.total_cost,
            description="Costo de mercaderías vendidas"
        )

        # Baja de stock
        JournalEntryLine.objects.create(
            entry=entry,
            account=get_account("MERCADERIAS"),
            credit=sale.total_cost,
            description="Baja de stock por venta"
        )

from django.contrib.auth.decorators import login_required

@login_required
def fiscal_invoice_list(request):
    invoices = FiscalInvoice.objects.select_related("customer", "sale").order_by("-date", "-id")
    return render(request, "fiscal/fiscal_invoice_list.html", {"invoices": invoices})


@login_required
def fiscal_invoice_detail(request, pk):
    invoice = get_object_or_404(FiscalInvoice, pk=pk)
    return render(request, "fiscal/fiscal_invoice_form.html", {"invoice": invoice})
