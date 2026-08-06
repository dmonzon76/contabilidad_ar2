from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.middleware.active_company import get_active_company_from_request

@login_required
def sales_dashboard(request):
    company = get_active_company_from_request(request)
    return render(
        request,
        "sales/dashboard.html",
        {"company": company}
    )
