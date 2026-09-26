from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from core.middleware.active_company import get_active_company_from_request
from fiscal.forms.thirdparty_tax_profile import ThirdPartyTaxProfileForm
from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile
from suppliers.forms.supplier import SupplierForm
from suppliers.models import Supplier


@login_required
def supplier_create(request):
    company = get_active_company_from_request(request)

    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                supplier = form.save(commit=False)
                supplier.company = company
                supplier.save()

                # Perfil fiscal predeterminado para el proveedor
                tax_profile = ThirdPartyTaxProfile.objects.create(
                    company=company,
                    afip_category="RI",
                )
                supplier.tax_profile = tax_profile
                supplier.save(update_fields=["tax_profile"])

            return redirect("purchases:supplier_tax_edit", supplier_id=supplier.id)
    else:
        form = SupplierForm()

    return render(request, "purchases/supplier_form.html", {"form": form})


@login_required
def supplier_tax_edit(request, supplier_id):
    company = get_active_company_from_request(request)
    supplier = get_object_or_404(Supplier, id=supplier_id, company=company)

    if supplier.tax_profile is None:
        supplier.tax_profile = ThirdPartyTaxProfile.objects.create(
            company=company,
            afip_category="RI",
        )
        supplier.save(update_fields=["tax_profile"])

    if request.method == "POST":
        form = ThirdPartyTaxProfileForm(request.POST, instance=supplier.tax_profile)
        if form.is_valid():
            form.save()
            return redirect("purchases:supplier_list")
    else:
        form = ThirdPartyTaxProfileForm(instance=supplier.tax_profile)

    return render(
        request,
        "purchases/supplier_tax_profile_form.html",
        {"supplier": supplier, "form": form},
    )
