from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from company.models import Company, CompanyActivity
from company.forms.activity import CompanyActivityForm
import json
from django.conf import settings


# ----------------------------------------
# Cargar tabla oficial AFIP desde JSON
# ----------------------------------------
def load_afip_codes():
    path = settings.BASE_DIR / "fiscal/data/afip_activities.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------
# LIST
# ----------------------------------------
@login_required
def activity_list(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    activities = company.activities.all()

    return render(request, "company/activity/list.html", {
        "company": company,
        "activities": activities,
    })


# ----------------------------------------
# CREATE
# ----------------------------------------
@login_required
def activity_create(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        form = CompanyActivityForm(request.POST)
        form.instance.company = company
        if form.is_valid():
            form.save()
            return redirect("company_activity_list", company_id=company.id)
    else:
        form = CompanyActivityForm()

    return render(request, "company/activity/create.html", {
        "company": company,
        "form": form,
        "afip_codes": load_afip_codes(),   # ← AUTOCOMPLETADO
    })


# ----------------------------------------
# EDIT
# ----------------------------------------
@login_required
def activity_edit(request, company_id, activity_id):
    company = get_object_or_404(Company, id=company_id)
    activity = get_object_or_404(CompanyActivity, id=activity_id, company=company)

    if request.method == "POST":
        form = CompanyActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("company_activity_list", company_id=company.id)
    else:
        form = CompanyActivityForm(instance=activity)

    return render(request, "company/activity/edit.html", {
        "company": company,
        "activity": activity,
        "form": form,
        "afip_codes": load_afip_codes(),   # ← AUTOCOMPLETADO
    })


# ----------------------------------------
# DELETE
# ----------------------------------------
@login_required
def activity_delete(request, company_id, activity_id):
    company = get_object_or_404(Company, id=company_id)
    activity = get_object_or_404(CompanyActivity, id=activity_id, company=company)

    if request.method == "POST":
        activity.delete()
        return redirect("company_activity_list", company_id=company.id)

    return render(request, "company/activity/delete.html", {
        "company": company,
        "activity": activity,
    })
