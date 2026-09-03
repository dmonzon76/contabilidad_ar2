from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from customers.models import Customer


def _customer_form_context(customer):
    return {
        "customer": customer,
        "iva_conditions": Customer._meta.get_field("iva_condition").choices,
    }


@login_required
def customer_list(request):
    customers = Customer.objects.filter(
        company=request.active_company,
        is_active=True,
    )
    return render(request, "customers/customer_list.html", {"customers": customers})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk, company=request.active_company)
    return render(request, "customers/customer_detail.html", {"customer": customer})


@login_required
def customer_add(request):
    company = request.active_company
    if request.method == "POST":
        customer = Customer(
            company=company,
            name=request.POST.get("name", "").strip(),
            tax_id=request.POST.get("tax_id", "").strip() or None,
            iva_condition=request.POST.get("iva_condition", "CF"),
            iibb_rate=request.POST.get("iibb_rate", "0") or 0,
            is_iibb_exempt=request.POST.get("is_iibb_exempt") == "on",
            ganancias_rate=request.POST.get("ganancias_rate", "0") or 0,
            is_ganancias_exempt=request.POST.get("is_ganancias_exempt") == "on",
            email=request.POST.get("email", "").strip() or None,
            phone=request.POST.get("phone", "").strip() or None,
            address=request.POST.get("address", "").strip() or None,
        )
        if customer.name:
            customer.save()
            return redirect("customers:customer_detail", customer.pk)
    return render(request, "customers/customer_form.html", _customer_form_context(None))


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk, company=request.active_company)
    if request.method == "POST":
        customer.name = request.POST.get("name", "").strip()
        customer.tax_id = request.POST.get("tax_id", "").strip() or None
        customer.iva_condition = request.POST.get("iva_condition", "CF")
        customer.iibb_rate = request.POST.get("iibb_rate", "0") or 0
        customer.is_iibb_exempt = request.POST.get("is_iibb_exempt") == "on"
        customer.ganancias_rate = request.POST.get("ganancias_rate", "0") or 0
        customer.is_ganancias_exempt = request.POST.get("is_ganancias_exempt") == "on"
        customer.email = request.POST.get("email", "").strip() or None
        customer.phone = request.POST.get("phone", "").strip() or None
        customer.address = request.POST.get("address", "").strip() or None
        if customer.name:
            customer.save()
            return redirect("customers:customer_detail", customer.pk)
    return render(
        request, "customers/customer_form.html", _customer_form_context(customer)
    )


@login_required
def customer_deactivate(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id,
        company=request.active_company,
    )
    if request.method == "POST":
        customer.is_active = False
        customer.save(update_fields=["is_active"])
    return redirect("customers:customer_list")


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk, company=request.active_company)
    if request.method == "POST":
        customer.delete()
        return redirect("customers:customer_list")
    return render(
        request, "customers/customer_confirm_delete.html", {"customer": customer}
    )
