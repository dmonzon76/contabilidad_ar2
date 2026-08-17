from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from fiscal.models import FiscalInvoice
from fiscal.forms import FiscalInvoiceForm


@login_required
def fiscal_invoice_list(request):
    invoices = FiscalInvoice.objects.select_related("customer", "voucher_book").order_by("-date")
    return render(request, "fiscal/fiscal_invoice_list.html", {
        "invoices": invoices,
    })


@login_required
def fiscal_invoice_create(request):
    if request.method == "POST":
        form = FiscalInvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fiscal:fiscal_invoice_list")
    else:
        form = FiscalInvoiceForm()

    return render(request, "fiscal/fiscal_invoice_form.html", {
        "form": form,
        "mode": "create",
    })


@login_required
def fiscal_invoice_edit(request, pk):
    invoice = get_object_or_404(FiscalInvoice, pk=pk)

    if request.method == "POST":
        form = FiscalInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect("fiscal:fiscal_invoice_list")
    else:
        form = FiscalInvoiceForm(instance=invoice)

    return render(request, "fiscal/fiscal_invoice_form.html", {
        "form": form,
        "mode": "edit",
        "invoice": invoice,
    })
