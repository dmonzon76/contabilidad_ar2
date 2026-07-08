from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from core.middleware.active_company import get_active_company_from_request

from sales.models.customer import Customer
from sales.forms.customer import CustomerForm
from fiscal.models import ThirdPartyTaxProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from core.middleware.active_company import get_active_company_from_request
from fiscal.forms.thirdparty_tax_profile import ThirdPartyTaxProfileForm
from sales.models.customer import Customer

# ---------------------------------------------------------
# LIST VIEW
# ---------------------------------------------------------
@login_required
def customer_list(request):
    """
    List all customers belonging to the active company.
    """
    company = get_active_company_from_request(request)
    customers = Customer.objects.filter(company=company).order_by("name")

    return render(request, "sales/customers/list.html", {
        "company": company,
        "customers": customers,
    })


# ---------------------------------------------------------
# CREATE VIEW
# ---------------------------------------------------------
@login_required
def customer_create(request):
    """
    Create a new customer for the active company.
    """
    company = get_active_company_from_request(request)

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
        customer = form.save(commit=False)
        customer.company = company
        customer.save()

    # Crear perfil fiscal automáticamente
    tax_profile = ThirdPartyTaxProfile.objects.create(
        company=company,
        customer=customer,   # si tu modelo lo soporta
        afip_category="RI",  # valor por defecto
        vat_21=False,
        vat_105=False,
        vat_27=False,
        vat_exempt=False,
        vat_non_taxed=False,
        ganancias_status="NO_APLICA",
        iibb_status="NO_APLICA",
        uses_perceptions=False,
        uses_retentions=False,
    )

    customer.tax_profile = tax_profile
    customer.save()

    return redirect("sales:customer_list")




@login_required
def customer_tax_edit(request, customer_id):
    company = get_active_company_from_request(request)
    customer = get_object_or_404(Customer, id=customer_id, company=company)

    tax_profile = customer.tax_profile

    if request.method == "POST":
        form = ThirdPartyTaxProfileForm(request.POST, instance=tax_profile)
        if form.is_valid():
            form.save()
            return redirect("sales:customer_edit", customer_id=customer.id)
    else:
        form = ThirdPartyTaxProfileForm(instance=tax_profile)

    return render(request, "sales/customers/tax_profile_form.html", {
        "company": company,
        "customer": customer,
        "form": form,
    })









    })


# ---------------------------------------------------------
# EDIT VIEW
# ---------------------------------------------------------
@login_required
def customer_edit(request, customer_id):
    """
    Edit an existing customer belonging to the active company.
    """
    company = get_active_company_from_request(request)
    customer = get_object_or_404(Customer, id=customer_id, company=company)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("sales:customer_list")
    else:
        form = CustomerForm(instance=customer)

    return render(request, "sales/customers/form.html", {
        "company": company,
        "form": form,
        "mode": "edit",
        "customer": customer,
    })


# ---------------------------------------------------------
# DELETE VIEW
# ---------------------------------------------------------
@login_required
def customer_delete(request, customer_id):
    """
    Delete a customer belonging to the active company.
    """
    company = get_active_company_from_request(request)
    customer = get_object_or_404(Customer, id=customer_id, company=company)

    if request.method == "POST":
        customer.delete()
        return redirect("sales:customer_list")

    return render(request, "sales/customers/delete.html", {
        "company": company,
        "customer": customer,
    })
