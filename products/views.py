from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})

def product_add(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("name"),
            sku=request.POST.get("sku"),
            description=request.POST.get("description"),
        )
        return redirect("product_list")

    return render(request, "products/product_add.html")
