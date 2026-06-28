from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounting.models import Account
from accounting.forms import AccountForm
from company.models import Company

from accounting.models.period import Period


# ---------------------------------------------------------
# LISTA (Árbol contable)
# ---------------------------------------------------------
@login_required
def account_list(request):
    company_id = request.session.get("active_company_id")
    accounts = Account.objects.filter(
        company_id=company_id,
        parent__isnull=True
    ).order_by("code")

    return render(request, "accounting/account_list.html", {
        "accounts": accounts
    })


# ---------------------------------------------------------
# CREAR CUENTA RAÍZ
# ---------------------------------------------------------
@login_required
def account_create(request):
    company_id = request.session["active_company_id"]
    company = Company.objects.get(id=company_id)

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.company = company
            acc.save()
            return redirect("account_list")
    else:
        form = AccountForm()

    return render(request, "accounting/account_create.html", {
        "form": form,
        "company": company,
    })


# ---------------------------------------------------------
# EDITAR CUENTA
# ---------------------------------------------------------
@login_required
def account_edit(request, account_id):
    company_id = request.session["active_company_id"]
    company = Company.objects.get(id=company_id)

    account = get_object_or_404(Account, id=account_id, company=company)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect("account_list")
    else:
        form = AccountForm(instance=account)

    return render(request, "accounting/account_edit.html", {
        "form": form,
        "company": company,
        "account": account,
    })


# ---------------------------------------------------------
# ELIMINAR CUENTA (solo si no tiene hijos)
# ---------------------------------------------------------
@login_required
def account_delete(request, account_id):
    company_id = request.session["active_company_id"]
    company = Company.objects.get(id=company_id)

    account = get_object_or_404(Account, id=account_id, company=company)

    if account.children.exists():
        return render(request, "accounting/account_delete_error.html", {
            "account": account,
            "company": company,
        })

    account.delete()
    return redirect("account_list")


# ---------------------------------------------------------
# NUEVO: CREAR SUBCUENTA (Add Child)
# ---------------------------------------------------------
@login_required
def account_add_child(request, parent_id):
    company_id = request.session["active_company_id"]
    company = Company.objects.get(id=company_id)

    parent = get_object_or_404(Account, id=parent_id, company=company)

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = parent
            child.company = company
            child.save()
            return redirect("account_list")
    else:
        # Código sugerido automáticamente
        existing_children = parent.children.order_by("code")
        if existing_children.exists():
            last_code = existing_children.last().code
            last_segment = int(last_code.split(".")[-1])
            suggested_code = parent.code + "." + str(last_segment + 1)
        else:
            suggested_code = parent.code + ".1"

        form = AccountForm(initial={
            "code": suggested_code,
            "account_type": parent.account_type,
        })

    return render(request, "accounting/account_add_child.html", {
        "form": form,
        "parent": parent,
        "company": company,
    })


# ---------------------------------------------------------
# PERIODOS (lo tuyo, intacto)
# ---------------------------------------------------------
def period_list(request):
    periods = Period.objects.select_related("fiscal_year").order_by("fiscal_year__year", "month")
    return render(request, "accounting/period_list.html", {"periods": periods})


def period_open(request, period_id):
    period = get_object_or_404(Period, id=period_id)
    period.status = "OPEN"
    period.save()
    return redirect("period_list")


def period_close(request, period_id):
    period = get_object_or_404(Period, id=period_id)
    period.status = "CLOSED"
    period.save()
    return redirect("period_list")


def period_lock(request, period_id):
    period = get_object_or_404(Period, id=period_id)
    period.status = "LOCKED"
    period.save()
    return redirect("period_list")
