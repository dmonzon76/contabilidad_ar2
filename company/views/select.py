from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company.models import Company
from django.http import HttpResponse, HttpResponseNotAllowed
import logging

logger = logging.getLogger(__name__)


@login_required
def select_company(request):

    # Acceso universal: mostrar todas las empresas
    companies = Company.objects.all()

    return render(
        request,
        "company/select.html",
        {
            "companies": companies,
        },
    )


@login_required
def set_active_company(request, company_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # No validamos CompanyUser porque no lo usamos más
    request.session["active_company_id"] = company_id

    return redirect("main_dashboard")


@login_required
def clear_select_modal_flag(request):
    logger.debug("clear_select_modal_flag called by %s", request.user)
    request.session.pop("show_company_select_modal", None)
    return HttpResponse("OK")
