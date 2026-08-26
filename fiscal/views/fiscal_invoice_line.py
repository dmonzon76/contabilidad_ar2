from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden

from fiscal.models import FiscalInvoice, FiscalInvoiceLine
from fiscal.forms import FiscalInvoiceLineForm
from core.utils import get_active_company


@login_required
@permission_required("fiscal.add_fiscalinvoiceline", raise_exception=True)
@require_http_methods(["GET", "POST"])
def fiscal_invoice_line_create(request, invoice_id):
    """
    Crea una línea fiscal validando:
    - autenticación
    - permisos
    - empresa activa
    - ownership del invoice (anti ID-guessing)
    - estado del invoice (no cerrado)
    """

    # 1) Validar empresa activa
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    # 2) Validar que la factura pertenece a la empresa activa
    invoice = get_object_or_404(FiscalInvoice, pk=invoice_id, company=company)

    # 3) Evitar agregar líneas a facturas cerradas
    if invoice.is_closed:
        return HttpResponseForbidden("Invoice is closed and cannot be modified")

    # 4) Procesar formulario
    if request.method == "POST":
        form = FiscalInvoiceLineForm(request.POST, company=company)
        if form.is_valid():
            line = form.save(commit=False)
            line.invoice = invoice
            line.company = company
            line.save()
            return redirect("fiscal:fiscal_invoice_edit", pk=invoice.id)
    else:
        form = FiscalInvoiceLineForm(company=company)

    return render(request, "fiscal/fiscal_invoice_line_form.html", {
        "form": form,
        "invoice": invoice,
    })


@login_required
@permission_required("fiscal.change_fiscalinvoiceline", raise_exception=True)
@require_http_methods(["GET", "POST"])
def fiscal_invoice_line_edit(request, pk):
    """
    Edita una línea fiscal validando:
    - autenticación
    - permisos
    - empresa activa
    - ownership del invoice y de la línea
    - estado del invoice
    """

    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    line = get_object_or_404(FiscalInvoiceLine, pk=pk, company=company)
    invoice = line.invoice

    if invoice.is_closed:
        return HttpResponseForbidden("Invoice is closed and cannot be modified")

    if request.method == "POST":
        form = FiscalInvoiceLineForm(request.POST, instance=line, company=company)
        if form.is_valid():
            form.save()
            return redirect("fiscal:fiscal_invoice_edit", pk=invoice.id)
    else:
        form = FiscalInvoiceLineForm(instance=line, company=company)

    return render(request, "fiscal/fiscal_invoice_line_form.html", {
        "form": form,
        "invoice": invoice,
        "line": line,
    })


@login_required
@permission_required("fiscal.delete_fiscalinvoiceline", raise_exception=True)
@require_http_methods(["POST"])
def fiscal_invoice_line_delete(request, pk):
    """
    Elimina una línea fiscal validando:
    - autenticación
    - permisos
    - empresa activa
    - ownership
    - estado del invoice
    """

    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    line = get_object_or_404(FiscalInvoiceLine, pk=pk, company=company)
    invoice = line.invoice

    if invoice.is_closed:
        return HttpResponseForbidden("Invoice is closed and cannot be modified")

    line.delete()
    return redirect("fiscal:fiscal_invoice_edit", pk=invoice.id)
