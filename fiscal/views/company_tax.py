from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from core.middleware.active_company import get_active_company_from_request
from fiscal.models.company_profile import CompanyProfile
from fiscal.forms.company_tax_profile import CompanyTaxProfileForm


@login_required
def company_tax_profile(request):
    # Obtener compañía activa desde middleware
    company = get_active_company_from_request(request)
    if company is None:
        return HttpResponseBadRequest("No active company selected.")

    # Garantizar perfil fiscal único
    profile, created = CompanyProfile.objects.get_or_create(company=company)

    if request.method == "POST":
        form = CompanyTaxProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("fiscal:company_tax_profile")
    else:
        form = CompanyTaxProfileForm(instance=profile)

    return render(
        request,
        "fiscal/company_tax_profile_form.html",
        {
            "company": company,
            "form": form,
            "profile": profile,
        },
    )
