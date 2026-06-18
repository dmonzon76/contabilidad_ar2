from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company.models import Company
import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    company_id = request.session.get("active_company_id")

    if not company_id:
        # Ask UI to show company selector as a modal on the dashboard
        request.session["show_company_select_modal"] = True
        active_company = None
    else:
        active_company = Company.objects.get(id=company_id)

    logger.debug(
        "Dashboard view: user=%s authenticated=%s sessionid=%s session_key=%s show_modal=%s session_keys=%s cookies=%s",
        request.user,
        request.user.is_authenticated,
        request.COOKIES.get("sessionid"),
        request.session.session_key,
        request.session.get("show_company_select_modal"),
        list(request.session.keys()),
        dict(request.COOKIES),
    )

    return render(request, "core/dashboard.html", {"active_company": active_company})


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")
