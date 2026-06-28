from django.shortcuts import render

# Create your views here.
# inventory/views.py



def product_list(request):
    return render(request, "inventory/product_list.html")
