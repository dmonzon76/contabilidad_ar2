from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from fiscal.models import FiscalProduct
from fiscal.forms import FiscalProductForm


@login_required
def fiscal_product_list(request):
    products = FiscalProduct.objects.all().order_by("name")
    return render(request, "fiscal/fiscal_product_list.html", {
        "products": products,
    })


@login_required
def fiscal_product_create(request):
    if request.method == "POST":
        form = FiscalProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fiscal:fiscal_product_list")
    else:
        form = FiscalProductForm()

    return render(request, "fiscal/fiscal_product_form.html", {
        "form": form,
        "mode": "create",
    })


@login_required
def fiscal_product_edit(request, pk):
    product = get_object_or_404(FiscalProduct, pk=pk)

    if request.method == "POST":
        form = FiscalProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("fiscal:fiscal_product_list")
    else:
        form = FiscalProductForm(instance=product)

    return render(request, "fiscal/fiscal_product_form.html", {
        "form": form,
        "mode": "edit",
        "product": product,
    })
