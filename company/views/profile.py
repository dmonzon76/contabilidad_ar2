from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from company.models import Company, CompanyProfile
from company.models import Company
from fiscal.models.company_profile import CompanyProfile
from fiscal.forms.company_tax_profile import CompanyTaxProfileForm

from core.utils.company_access import user_has_access


@login_required
# company/views/profile.py
def company_tax_profile_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    # Si no existe el perfil, lo crea automáticamente
    profile, created = CompanyProfile.objects.get_or_create(company=company)

    context = {
        "company": company,
        "profile": profile,
        "created": created,  # opcional, por si querés mostrar un mensaje
    }

    return render(request, "company/profile/view.html", context)



@login_required
def company_tax_profile_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    profile, created = CompanyProfile.objects.get_or_create(company=company)

    if request.method == "POST":
        profile.cuit = request.POST.get("cuit")
        profile.iibb = request.POST.get("iibb")
        profile.afip_category = request.POST.get("afip_category")
        profile.save()
        return redirect("company:company_tax_profile", company_id=company.id)

    return render(request, "company/profile/edit.html", {
        "company": company,
        "profile": profile,
    })








