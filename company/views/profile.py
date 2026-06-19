from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from company.forms import CompanyProfileForm
from company.models.models import Company, CompanyProfile


@login_required
def profile_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    profile = company.tax_profile
    return render(request, "company/profile/view.html", {
        "company": company,
        "profile": profile,
    })


@login_required
def profile_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    profile = company.tax_profile

    if request.method == "POST":
        form = CompanyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("company_profile", company_id=company.id)  # ← CORREGIDO
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, "company/profile/edit.html", {
        "company": company,
        "form": form,
    })
