from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from customers.forms import CustomerForm
from customers.models import Customer


@login_required
def customer_list(request):
    customers = Customer.objects.filter(
        company=request.active_company,
    )
    return render(request, "customers/customer_list.html", {"customers": customers})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk, company=request.active_company)
    return render(request, "customers/customer_detail.html", {"customer": customer})


@login_required
def customer_add(request):
    company = request.active_company
    form = CustomerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            customer = form.save(commit=False)
            customer.company = company
            customer.save()
            return redirect("customers:customer_detail", customer.pk)
    return render(
        request,
        "customers/customer_form.html",
        {"form": form, "customer": None},
    )


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk, company=request.active_company)
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("customers:customer_detail", customer.pk)
    return render(
        request,
        "customers/customer_form.html",
        {"form": form, "customer": customer},
    )


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk, company=request.active_company)
    if request.method == "POST":
        customer.delete()
        return redirect("customers:customer_list")
    return render(
        request, "customers/customer_confirm_delete.html", {"customer": customer}
    )
