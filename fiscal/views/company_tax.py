from django.shortcuts import render, redirect, get_object_or_404
from fiscal.models import CompanyProfile
from fiscal.forms import CompanyProfileForm
from company.models import Company


def company_tax_profile_view(request):
    company_id = request.session.get("active_company_id")
    company = get_object_or_404(Company, id=company_id)

    profile, created = CompanyProfile.objects.get_or_create(company=company)

    return render(request, "fiscal/company_tax_profile.html", {
        "company": company,
        "profile": profile,
    })


def company_tax_profile_edit(request):
    company_id = request.session.get("active_company_id")
    company = get_object_or_404(Company, id=company_id)

    profile, created = CompanyProfile.objects.get_or_create(company=company)

    if request.method == "POST":
        form = CompanyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("company_tax_profile")
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, "fiscal/company_tax_profile_form.html", {
        "form": form,
        "company": company,
    })
