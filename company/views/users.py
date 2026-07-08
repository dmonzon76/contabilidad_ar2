from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from company.models import Company, CompanyUser
from company.forms.user import CompanyUserForm
from core.utils.company_access import user_has_access


@login_required
def company_user_list(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    users = CompanyUser.objects.filter(company=company)

    return render(request, "company/users/list.html", {
        "company": company,
        "users": users,
    })


@login_required
def company_user_create(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    if request.method == "POST":
        form = CompanyUserForm(request.POST)
        form.instance.company = company
        if form.is_valid():
            form.save()
            return redirect("company:company_user_list", company_id=company.id)
    else:
        form = CompanyUserForm()

    return render(request, "company/users/create.html", {
        "company": company,
        "form": form,
    })


@login_required
def company_user_edit(request, company_id, user_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    user = get_object_or_404(CompanyUser, id=user_id, company=company)

    if request.method == "POST":
        form = CompanyUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("company:company_user_list", company_id=company.id)
    else:
        form = CompanyUserForm(instance=user)

    return render(request, "company/users/edit.html", {
        "company": company,
        "form": form,
        "user": user,
    })


@login_required
def company_user_delete(request, company_id, user_id):
    company = get_object_or_404(Company, id=company_id)

    if not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    user = get_object_or_404(CompanyUser, id=user_id, company=company)

    if request.method == "POST":
        user.delete()
        return redirect("company:company_user_list", company_id=company.id)

    return render(request, "company/users/delete.html", {
        "company": company,
        "user": user,
    })
