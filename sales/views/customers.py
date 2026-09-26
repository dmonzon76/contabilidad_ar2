from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from fiscal.forms.thirdparty_tax_profile import ThirdPartyTaxProfileForm
from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile
from sales.forms.customer import CustomerForm
from sales.models.customer import Customer


@login_required
def customer_list(request):
    """
    Lista los clientes pertenecientes a la empresa activa.
    """
    company_id = request.session.get("active_company_id")
    customers = Customer.objects.filter(company_id=company_id, is_active=True)
    return render(
        request,
        "sales/customers/customer_list.html",
        {"customers": customers}
    )


@login_required
def customer_create(request):
    """
    Crea un nuevo cliente y le asigna su perfil fiscal automáticamente.
    """
    company_id = request.session.get("active_company_id")

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                customer = form.save(commit=False)
                customer.company_id = company_id
                customer.save()

                tax_profile = ThirdPartyTaxProfile.objects.create(
                    company_id=company_id,
                    afip_category="RI",
                )
                customer.tax_profile = tax_profile
                customer.save(update_fields=["tax_profile"])

            return redirect("sales:customer_list")
    else:
        form = CustomerForm()

    return render(
        request,
        "sales/customers/form.html",
        {"form": form, "mode": "create"}
    )


@login_required
def customer_edit(request, customer_id):
    """
    Edita los datos generales de un cliente existente.
    """
    company_id = request.session.get("active_company_id")
    customer = get_object_or_404(Customer, id=customer_id, company_id=company_id)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("sales:customer_list")
    else:
        form = CustomerForm(instance=customer)

    return render(
        request,
        "sales/customers/form.html",
        {"form": form, "mode": "edit", "customer": customer}
    )


@login_required
def customer_tax_edit(request, customer_id):
    """
    Edita el perfil fiscal del cliente.
    """
    company_id = request.session.get("active_company_id")
    customer = get_object_or_404(Customer, id=customer_id, company_id=company_id)

    if not customer.tax_profile:
        customer.tax_profile = ThirdPartyTaxProfile.objects.create(
            company_id=company_id,
            afip_category="RI",
        )
        customer.save(update_fields=["tax_profile"])

    if request.method == "POST":
        form = ThirdPartyTaxProfileForm(request.POST, instance=customer.tax_profile)
        if form.is_valid():
            form.save()
            return redirect("sales:customer_list")
    else:
        form = ThirdPartyTaxProfileForm(instance=customer.tax_profile)

    return render(
        request,
        "sales/customers/tax_profile_form.html",
        {"customer": customer, "form": form}
    )
