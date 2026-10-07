from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from company.models import Company, CompanyUser


@login_required
def select_company_list(request):
    """
    Muestra únicamente las empresas a las que el usuario autenticado
    tiene acceso activo.
    """
    user_companies = CompanyUser.objects.filter(user=request.user, is_active=True).select_related("company")

    companies = [uc.company for uc in user_companies]

    return render(
        request,
        "company/select.html",
        {
            "companies": companies,
            "active_company_id": request.session.get("active_company_id"),
        },
    )


@login_required
@require_POST
def select_company(request, company_id):
    """
    Activa una empresa en la sesión únicamente si el usuario pertenece a ella.
    """
    has_access = CompanyUser.objects.filter(user=request.user, company_id=company_id, is_active=True).exists()

    if not has_access:
        raise PermissionDenied("No tenés permisos para acceder a esta empresa.")

    company = get_object_or_404(Company, pk=company_id)

    request.session["active_company_id"] = company.id
    request.session.pop("show_company_select_modal", None)
    messages.success(request, f"Empresa activa cambiada a: {company.name}")

    next_url = request.POST.get("next") or request.GET.get("next") or "main_dashboard"
    try:
        return redirect(next_url)
    except Exception:
        return redirect("main_dashboard")


@login_required
def clear_select_modal_flag(request):
    """
    Limpia la bandera de sesión del modal flotante.
    """
    request.session.pop("show_company_select_modal", None)
    return JsonResponse({"status": "ok"})


# Alias de compatibilidad
set_active_company = select_company
