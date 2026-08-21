from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from products.forms import ProductForm
from core.middleware.active_company import get_active_company_from_request


def product_list(request):
    company = get_active_company_from_request(request)
    products = Product.objects.filter(company=company)
    return render(request, "products/product_list.html", {"products": products})


def product_add(request):
    company = get_active_company_from_request(request)

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.company = company
            p.save()
            return redirect("products:product_list")
    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {"form": form})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_form.html", {"form": form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("products:product_list")

    return render(request, "products/product_delete.html", {"product": product})
