from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from sales.models import Sale
from fiscal.models import FiscalInvoice
from accounting.models import JournalEntry
from company.models import Company


@login_required
def dashboard(request):
    today = now().date()
    company_id = request.session.get("active_company_id")

    if not company_id:
        return redirect("company:company_select")

    company = get_object_or_404(Company, id=company_id)

    # --- Sales KPIs ---
    sales_qs = Sale.objects.filter(company_id=company_id)
    sales_today = sales_qs.filter(date=today).count()
    sales_month = sales_qs.filter(
        date__year=today.year, date__month=today.month
    ).count()

    # --- Fiscal KPIs ---
    fiscal_today = FiscalInvoice.objects.filter(
        company_id=company_id, date=today
    ).count()

    # --- Accounting KPIs ---
    journal_today = JournalEntry.objects.filter(
        company_id=company_id, date=today
    ).count()

    context = {
        "sales_today": sales_today,
        "sales_month": sales_month,
        "fiscal_today": fiscal_today,
        "journal_today": journal_today,
        "company": company,
    }

    return render(request, "core/dashboard.html", context)
