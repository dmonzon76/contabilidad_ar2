from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from accounting.forms import FiscalYearForm
from accounting.models import FiscalYear
from core.utils.company_access import user_has_access


@login_required
def fiscal_year_create(request):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    form = FiscalYearForm(request.POST or None, company=company)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            fiscal_year = form.save(commit=False)
            fiscal_year.company = company
            fiscal_year.status = "OPEN"
            fiscal_year.save()

        messages.success(
            request,
            f"Fiscal year {fiscal_year.year} and its 12 periods were created.",
        )
        return redirect("accounting:fiscal_year_list")

    return render(
        request,
        "accounting/fiscal_year_create.html",
        {"form": form, "company": company},
    )
