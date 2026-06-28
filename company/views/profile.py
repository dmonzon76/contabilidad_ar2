from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from fiscal.models import CompanyProfile
from company.models import Company
from fiscal.forms import CompanyProfileForm
from core.utils.company_access import user_has_access


@login_required
def company_tax_profile_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    profile = get_object_or_404(CompanyProfile, company=company)

    return render(request, "fiscal/company_tax_profile.html", {
        "company": company,
        "profile": profile,
    })


@login_required
def company_tax_profile_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    profile = get_object_or_404(CompanyProfile, company=company)

    if request.method == "POST":
        form = CompanyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("company_tax_profile", company_id=company.id)
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, "fiscal/company_tax_profile_form.html", {
        "company": company,
        "form": form,
    })
