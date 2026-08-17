from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from fiscal.models import FiscalInvoiceLine, FiscalInvoice
from fiscal.forms import FiscalInvoiceLineForm


@login_required
def fiscal_invoice_line_create(request, invoice_id):
    invoice = get_object_or_404(FiscalInvoice, pk=invoice_id)

    if request.method == "POST":
        form = FiscalInvoiceLineForm(request.POST)
        if form.is_valid():
            line = form.save(commit=False)
            line.invoice = invoice
            line.save()
            return redirect("fiscal:fiscal_invoice_edit", pk=invoice.id)
    else:
        form = FiscalInvoiceLineForm()

    return render(request, "fiscal/fiscal_invoice_line_form.html", {
        "form": form,
        "invoice": invoice,
    })
