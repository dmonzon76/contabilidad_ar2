from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from fiscal.models import FiscalSale
from fiscal.forms import FiscalSaleForm


@login_required
def fiscal_sale_list(request):
    sales = FiscalSale.objects.select_related("sale", "voucher_book", "invoice").order_by("-id")
    return render(request, "fiscal/fiscal_sale_list.html", {
        "sales": sales,
    })


@login_required
def fiscal_sale_create(request):
    if request.method == "POST":
        form = FiscalSaleForm(request.POST)
        if form.is_valid():
            fiscal_sale = form.save()
            return redirect("fiscal:fiscal_sale_list")
    else:
        form = FiscalSaleForm()

    return render(request, "fiscal/fiscal_sale_form.html", {
        "form": form,
        "mode": "create",
    })


@login_required
def fiscal_sale_generate_invoice(request, pk):
    fiscal_sale = get_object_or_404(FiscalSale, pk=pk)
    invoice = fiscal_sale.generate_invoice()
    return redirect("fiscal:fiscal_invoice_edit", pk=invoice.id)
