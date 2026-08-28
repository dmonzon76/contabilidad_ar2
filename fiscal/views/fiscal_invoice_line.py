from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden

from fiscal.models import FiscalInvoice, FiscalInvoiceLine
from fiscal.forms import FiscalInvoiceLineForm

from core.utils.company_active import get_active_company
from core.utils.company_access import user_has_access

@login_required
@permission_required("fiscal.add_fiscalinvoiceline", raise_exception=True)
@require_http_methods(["GET", "POST"])
def fiscal_invoice_line_create(request, invoice_id):

    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

    invoice = get_object_or_404(FiscalInvoice, pk=invoice_id, company=company)

    if invoice.is_closed:
        return HttpResponseForbidden("Invoice is closed and cannot be modified")

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


# Compatibilidad con URLs de código anterior.
fiscal_invoice_line_add = fiscal_invoice_line_create


@login_required
@permission_required("fiscal.change_fiscalinvoiceline", raise_exception=True)
@require_http_methods(["GET", "POST"])
def fiscal_invoice_line_edit(request, pk):

    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

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

    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

    line = get_object_or_404(FiscalInvoiceLine, pk=pk, company=company)
    invoice = line.invoice

    if invoice.is_closed:
        return HttpResponseForbidden("Invoice is closed and cannot be modified")

    line.delete()
    return redirect("fiscal:fiscal_invoice_edit", pk=invoice.id)
