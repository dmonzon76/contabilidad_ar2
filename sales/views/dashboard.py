from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from core.utils.company_access import user_has_access
from sales.models import Customer, Sale


@login_required
def sales_dashboard(request):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    sales = Sale.objects.filter(company=company)
    current_month = timezone.localdate().replace(day=1)
    current_month_sales = sales.filter(date__gte=current_month)

    context = {
        "company": company,
        "sales_count": sales.count(),
        "sales_total": sales.aggregate(total=Sum("total_amount"))["total"] or 0,
        "current_month_total": current_month_sales.aggregate(total=Sum("total_amount"))[
            "total"
        ]
        or 0,
        "customers_count": Customer.objects.filter(
            company=company, is_active=True
        ).count(),
        "recent_sales": sales.select_related("customer")[:5],
    }

    return render(request, "sales/dashboard.html", context)
