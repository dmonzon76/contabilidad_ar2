from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company.models import CompanyUser
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


@login_required
def select_company(request):

    companies = CompanyUser.objects.filter(
        user=request.user, is_active=True
    ).select_related("company")
    # Always show selection UI even if user has a single company
    return render(
        request,
        "company/select.html",
        {
            "companies": companies,
        },
    )


@login_required
def set_active_company(request, company_id):

    # Validate access
    if CompanyUser.objects.filter(
        user=request.user, company_id=company_id, is_active=True
    ).exists():
        request.session["active_company_id"] = company_id

    return redirect("dashboard")


@login_required
def clear_select_modal_flag(request):
    logger.debug("clear_select_modal_flag called by %s", request.user)
    request.session.pop("show_company_select_modal", None)
    return HttpResponse("OK")
