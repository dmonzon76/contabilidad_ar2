from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from company.models import Company, CompanyProfile, CompanyUser
from core.utils.company_access import user_has_access


@login_required
def company_list(request):
    companies = Company.objects.filter(
        company_users__user=request.user,
        company_users__is_active=True,
    )
    return render(request, "company/company_list.html", {"companies": companies})


@login_required
def company_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        tax_id = request.POST.get("tax_id")
        afip_category = request.POST.get("afip_category")
        address = request.POST.get("address")
        city = request.POST.get("city")
        province = request.POST.get("province")

        company = Company.objects.create(
            name=name,
            tax_id=tax_id,
            afip_category=afip_category,
            address=address,
            city=city,
            province=province,
        )

        # Crear perfil fiscal vacío
        CompanyProfile.objects.create(company=company)
        CompanyUser.objects.create(
            user=request.user,
            company=company,
            role="OWNER",
        )
        request.session["active_company_id"] = company.id

        return redirect("company:company_list")

    return render(request, "company/company_create.html")


@login_required
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    # Seguridad multi-company
    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    return render(
        request,
        "company/company_detail.html",
        {
            "company": company,
        },
    )


@login_required
def company_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    if request.method == "POST":
        company.name = request.POST.get("name")
        company.tax_id = request.POST.get("tax_id")
        company.afip_category = request.POST.get("afip_category")
        company.address = request.POST.get("address")
        company.city = request.POST.get("city")
        company.province = request.POST.get("province")
        company.save()

        return redirect("company:company_detail", company_id=company.id)

    return render(request, "company/company_edit.html", {"company": company})
