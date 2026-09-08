from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounting.models import Account
from accounting.forms import AccountForm
from company.models import Company
from accounting.models.period import Period
from core.utils.company_access import user_has_access


# ============================================================
# ACCOUNTS
# ============================================================

@login_required
def account_list(request):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    accounts = Account.objects.filter(
        company=company,
        parent__isnull=True
    ).order_by("code")

    return render(request, "accounting/account_list.html", {
        "company": company,
        "accounts": accounts,
    })


@login_required
def account_create(request):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.company = company
            acc.save()
            return redirect("accounting:account_list")
    else:
        form = AccountForm()

    return render(request, "accounting/account_create.html", {
        "form": form,
        "company": company,
    })


@login_required
def account_edit(request, account_id):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    account = get_object_or_404(Account, id=account_id, company=company)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect("accounting:account_list")
    else:
        form = AccountForm(instance=account)

    return render(request, "accounting/account_edit.html", {
        "form": form,
        "company": company,
        "account": account,
    })


@login_required
def account_delete(request, account_id):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    account = get_object_or_404(Account, id=account_id, company=company)

    if account.children.exists():
        return render(request, "accounting/account_delete_error.html", {
            "account": account,
            "company": company,
        })

    account.delete()
    return redirect("accounting:account_list")


@login_required
def account_add_child(request, parent_id):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    parent = get_object_or_404(Account, id=parent_id, company=company)

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = parent
            child.company = company
            child.save()
            return redirect("accounting:account_list")
    else:
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


# ============================================================
# PERIODS (ANUALES)
# ============================================================

@login_required
def period_list(request):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    periods = Period.objects.filter(
        fiscal_year__company=company
    ).select_related("fiscal_year").order_by(
        "fiscal_year__start_date"
    )

    return render(request, "accounting/period_list.html", {
        "company": company,
        "periods": periods,
    })


@login_required
def period_open(request, period_id):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    period = get_object_or_404(Period, id=period_id, fiscal_year__company=company)
    period.status = "OPEN"
    period.save()
    return redirect("accounting:period_list")


@login_required
def period_close(request, period_id):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    period = get_object_or_404(Period, id=period_id, fiscal_year__company=company)
    period.status = "CLOSED"
    period.save()
    return redirect("accounting:period_list")


@login_required
def period_lock(request, period_id):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    period = get_object_or_404(Period, id=period_id, fiscal_year__company=company)
    period.status = "LOCKED"
    period.save()
    return redirect("accounting:period_list")
