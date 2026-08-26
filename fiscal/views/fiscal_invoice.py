from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from fiscal.models.fiscal_invoice import FiscalInvoice
from sales.models.sale import Sale

from accounting.models.journal import JournalEntry, JournalEntryLine
from accounting.models.account import Account
from accounting.models.period import Period

from core.utils import get_active_company


def get_account(code):
    """Obtiene la cuenta contable por código."""
    return Account.objects.get(code=code)


def current_period(company):
    """Obtiene el período contable activo."""
    return Period.objects.get_current(company=company)


@login_required
@permission_required("fiscal.add_fiscalinvoice", raise_exception=True)
@require_POST
def fiscal_invoice_create(request, sale_id):
    """
    Crea una factura fiscal validando:
    - autenticación
    - permisos
    - empresa activa
    - ownership de la venta (anti ID-guessing)
    - duplicación de facturas
    """

    # 1) Validar empresa activa
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    # 2) Validar que la venta pertenece a la empresa activa
    sale = get_object_or_404(Sale, id=sale_id, company=company)

    # 3) Evitar duplicación
    if hasattr(sale, "fiscal_invoice"):
        return redirect("sales:sale_detail", pk=sale.id)

    # 4) Configuración fiscal (puede venir de la empresa)
    voucher_type = "B"
    point_of_sale = 1

    # 5) Numeración fiscal segura
    voucher_number = FiscalInvoice.next_number(
        company=company,
        point_of_sale=point_of_sale,
        voucher_type=voucher_type
    )

    # 6) Crear factura fiscal
    invoice = FiscalInvoice.objects.create(
        company=company,
        customer=sale.customer,
        sale=sale,
        voucher_type=voucher_type,
        point_of_sale=point_of_sale,
        voucher_number=voucher_number,
    )

    # 7) Calcular totales y CAE
    invoice.finalize()

    # 8) Generar asiento contable automático
    generate_accounting_entry(invoice, request.user)

    return redirect("sales:sale_detail", pk=sale.id)


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


@login_required
@permission_required("fiscal.view_fiscalinvoice", raise_exception=True)
def fiscal_invoice_list(request):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    invoices = FiscalInvoice.objects.filter(company=company).select_related("customer", "sale").order_by("-date", "-id")
    return render(request, "fiscal/fiscal_invoice_list.html", {"invoices": invoices})


@login_required
@permission_required("fiscal.view_fiscalinvoice", raise_exception=True)
def fiscal_invoice_detail(request, pk):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    invoice = get_object_or_404(FiscalInvoice, pk=pk, company=company)
    return render(request, "fiscal/fiscal_invoice_form.html", {"invoice": invoice})
