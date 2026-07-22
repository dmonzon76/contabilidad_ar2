from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier})

def supplier_add(request):
    if request.method == 'POST':
        Supplier.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
        )
        return redirect('supplier_list')

    return render(request, 'suppliers/supplier_add.html')

