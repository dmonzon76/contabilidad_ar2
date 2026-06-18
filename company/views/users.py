from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from company.models import Company, CompanyUser
from company.forms import CompanyUserForm


# ============================================================
# LIST
# ============================================================
@login_required
def company_user_list(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    users = company.company_users.select_related("user")

    return render(request, "company/users/list.html", {
        "company": company,
        "users": users,
    })


# ============================================================
# CREATE
# ============================================================
@login_required
def company_user_create(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        form = CompanyUserForm(request.POST)
        if form.is_valid():
            cu = form.save(commit=False)
            cu.company = company
            cu.save()
            return redirect("company_user_list", company_id=company.id)
    else:
        form = CompanyUserForm()

    return render(request, "company/users/create.html", {
        "company": company,
        "form": form,
    })


# ============================================================
# EDIT
# ============================================================
@login_required
def company_user_edit(request, company_id, user_id):
    company = get_object_or_404(Company, id=company_id)
    cu = get_object_or_404(CompanyUser, id=user_id, company=company)

    if request.method == "POST":
        form = CompanyUserForm(request.POST, instance=cu)
        if form.is_valid():
            form.save()
            return redirect("company_user_list", company_id=company.id)
    else:
        form = CompanyUserForm(instance=cu)

    return render(request, "company/users/edit.html", {
        "company": company,
        "form": form,
        "cu": cu,
    })


# ============================================================
# DELETE
# ============================================================
@login_required
def company_user_delete(request, company_id, user_id):
    company = get_object_or_404(Company, id=company_id)
    cu = get_object_or_404(CompanyUser, id=user_id, company=company)

    cu.delete()
    return redirect("company_user_list", company_id=company.id)
