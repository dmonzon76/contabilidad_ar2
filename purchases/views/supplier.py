from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from purchases.models import Supplier
from core.middleware.active_company import get_active_company_from_request
from suppliers.forms.supplier import SupplierForm
from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile
from fiscal.forms.thirdparty_tax_profile import ThirdPartyTaxProfileForm


@login_required
def supplier_list(request):
    company = get_active_company_from_request(request)
    suppliers = Supplier.objects.filter(company=company, is_active=True).order_by(
        "name"
    )
    return render(request, "purchases/supplier_list.html", {"suppliers": suppliers})


@login_required
def supplier_create(request):
    company = get_active_company_from_request(request)

    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.company = company
            supplier.save()

            tax_profile = ThirdPartyTaxProfile.objects.create(
                company=company,
                afip_category="RI",
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
            supplier.tax_profile = tax_profile
            supplier.save()
            return redirect("purchases:supplier_tax_edit", supplier_id=supplier.id)
    else:
        form = SupplierForm()

    return render(request, "purchases/supplier_form.html", {"form": form})


@login_required
def supplier_edit(request, supplier_id):
    company = get_active_company_from_request(request)
    supplier = get_object_or_404(Supplier, id=supplier_id, company=company)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect("purchases:supplier_list")
    else:
        form = SupplierForm(instance=supplier)

    return render(
        request, "purchases/supplier_form.html", {"form": form, "supplier": supplier}
    )


@login_required
def supplier_tax_edit(request, supplier_id):
    company = get_active_company_from_request(request)
    supplier = get_object_or_404(Supplier, id=supplier_id, company=company)
    tax_profile = supplier.tax_profile

    if request.method == "POST":
        form = ThirdPartyTaxProfileForm(request.POST, instance=tax_profile)
        if form.is_valid():
            form.save()
            return redirect("purchases:supplier_list")
    else:
        form = ThirdPartyTaxProfileForm(instance=tax_profile)

    return render(
        request,
        "purchases/supplier_tax_profile_form.html",
        {"supplier": supplier, "form": form},
    )
