from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounting.models import FiscalYear, Period, JournalEntry, Account
from core.utils.company_access import user_has_access


@login_required
def accounting_dashboard(request):
    """
    Main dashboard for the Accounting module.
    Shows current fiscal year, current period, and quick stats.
    """

    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    current_fy = FiscalYear.objects.filter(
        company=company, status="OPEN"
    ).order_by("-start_date").first()
    current_period = Period.objects.filter(
        fiscal_year__company=company, status="OPEN"
    ).order_by("-start_date").first()

    context = {
        "current_fiscal_year": current_fy,
        "current_period": current_period,
        "company": company,
        "journal_entries_count": JournalEntry.objects.filter(company=company).count(),
        "accounts_count": Account.objects.filter(company=company).count(),
    }

    return render(request, "accounting/dashboard.html", context)


def fiscal_year_list(request):
    """
    List of fiscal years (annual only).
    """
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)
    fiscal_years = FiscalYear.objects.filter(company=company).order_by("-start_date")
    return render(request, "accounting/fiscal_year_list.html", {"fiscal_years": fiscal_years})


def fiscal_year_open(request, fiscal_year_id):
    """
    Open a fiscal year.
    """
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)
    fy = get_object_or_404(FiscalYear, pk=fiscal_year_id, company=company)
    fy.status = "OPEN"
    fy.save()

    # Ensure the period is also opened
    period = Period.objects.filter(fiscal_year=fy).first()
    if period:
        period.status = "OPEN"
        period.save()

    messages.success(request, f"Fiscal year {fy.year} opened.")
    return redirect("accounting:fiscal_year_list")


def fiscal_year_close(request, fiscal_year_id):
    """
    Close a fiscal year.
    """
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)
    fy = get_object_or_404(FiscalYear, pk=fiscal_year_id, company=company)
    fy.status = "CLOSED"
    fy.save()

    # Close the period too
    period = Period.objects.filter(fiscal_year=fy).first()
    if period:
        period.status = "CLOSED"
        period.save()

    messages.success(request, f"Fiscal year {fy.year} closed.")
    return redirect("accounting:fiscal_year_list")
