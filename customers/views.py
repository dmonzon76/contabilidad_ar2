from django.shortcuts import render, get_object_or_404, redirect
from customers.models import Customer   # ✔ tu modelo real está en accounting


def customer_list(request):
    customers = Customer.objects.filter(is_active=True)
    return render(request, 'sales/customers/list.html', {'customers': customers})


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'sales/customers/detail.html', {'customer': customer})


def customer_add(request):
    if request.method == 'POST':
        Customer.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            is_active=True
        )
        return redirect('sales:customer_list')

    return render(request, 'sales/customers/add.html')


def customer_deactivate(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_active = False
    customer.save()
    return redirect("sales:customer_list")
