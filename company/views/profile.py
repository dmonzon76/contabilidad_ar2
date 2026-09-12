from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from company.models import Company
from fiscal.models.company_profile import CompanyProfile
from fiscal.forms.company_tax_profile import CompanyTaxProfileForm

from core.utils.company_access import user_has_access


@login_required
def company_tax_profile_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return redirect("no_access")

    profile = get_object_or_404(CompanyProfile, company=company)

    return render(
        request,
        "fiscal/company_tax_profile.html",
        {
            "company": company,
            "profile": profile,
        },
    )


@login_required
def company_tax_profile_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request.user, company):
        return redirect("no_access")

    profile = get_object_or_404(CompanyProfile, company=company)

    if request.method == "POST":
        form = CompanyTaxProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("company:company_tax_profile", company_id=company.id)
    else:
        form = CompanyTaxProfileForm(instance=profile)

    context = {
        "company": company,
        "form": form,
        "profile": profile,
    }
    return render(request, "fiscal/company_tax_profile_form.html", context)
