from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from accounting.forms import FiscalYearForm
from accounting.models import FiscalYear, Period
from core.utils.company_access import user_has_access


class FiscalYearService:
    @staticmethod
    def create_year(company, year):
        fiscal_year, _ = FiscalYear.objects.get_or_create(
            company=company,
            year=year,
            defaults={
                "start_date": date(year, 1, 1),
                "end_date": date(year, 12, 31),
                "status": "OPEN",
            },
        )

        from calendar import monthrange

        for month in range(1, 13):

            Period.objects.get_or_create(
                fiscal_year=fiscal_year,
                month=month,
                defaults={
                    "start_date": date(year, month, 1),
                    "end_date": date(
                        year,
                        month,
                        monthrange(year, month)[1],
                    ),
                    "status": "OPEN",
                },
            )

        return fiscal_year


@login_required
def fiscal_year_create(request):

    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(
            request,
            "errors/403.html",
            status=403,
        )

    form = FiscalYearForm(
        request.POST or None,
        company=company,
    )

    if request.method == "POST" and form.is_valid():

        with transaction.atomic():

            fiscal_year = FiscalYearService.create_year(
                company=company,
                year=form.cleaned_data["year"],
            )

        messages.success(
            request,
            f"Fiscal year {fiscal_year.year} and its 12 periods were created."
        )

        return redirect(
            "accounting:fiscal_year_list"
        )

    return render(
        request,
        "accounting/fiscal_year_create.html",
        {
            "form": form,
            "company": company,
        },
    )