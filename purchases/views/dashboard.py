from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from core.utils.company_access import user_has_access
from suppliers.models import Supplier

from purchases.models import Purchase


@login_required
def purchases_dashboard(request):
    company = request.active_company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    purchases = Purchase.objects.filter(company=company, is_active=True)
    current_month = timezone.localdate().replace(day=1)
    current_month_purchases = purchases.filter(date__gte=current_month)

    context = {
        "company": company,
        "purchases_count": purchases.count(),
        "purchases_total": purchases.aggregate(total=Sum("total_amount"))["total"] or 0,
        "current_month_total": current_month_purchases.aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0,
        "suppliers_count": Supplier.objects.filter(
            company=company, is_active=True
        ).count(),
        "recent_purchases": purchases.select_related("supplier")[:5],
    }

    return render(request, "purchases/dashboard.html", context)
