from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from core.utils.company_access import user_has_access
from customers.models import Customer
from sales.models.sale import Sale


@login_required
def sales_dashboard(request):

    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(
            request,
            "errors/403.html",
            status=403,
        )

    sales = Sale.objects.filter(
        company=company,
    )

    current_month = timezone.localdate().replace(
        day=1,
    )

    current_month_sales = sales.filter(
        date__gte=current_month,
    )

    draft_sales = sales.filter(
        status="DRAFT",
    )

    issued_sales = sales.filter(
        status="ISSUED",
    )

    context = {
        "company": company,
        # KPI
        "draft_sales_count": draft_sales.count(),
        "issued_sales_count": issued_sales.count(),
        "credit_notes_count": 0,  # Placeholder
        "sales_count": sales.count(),
        "sales_total": sales.aggregate(total=Sum("total_amount"))["total"] or 0,
        "current_month_total": current_month_sales.aggregate(total=Sum("total_amount"))["total"] or 0,
        "customers_count": Customer.objects.filter(
            company=company,
        ).count(),
        # Recent Activity
        "recent_sales": sales.select_related(
            "customer",
        )[:10],
    }

    return render(
        request,
        "sales/dashboard.html",
        context,
    )
