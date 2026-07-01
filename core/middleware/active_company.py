from django.shortcuts import redirect
from django.urls import reverse
from company.models.models import CompanyUser


class ActiveCompanyMiddleware:
    """
    Middleware que asegura que el usuario tenga una empresa activa seleccionada.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Rutas que NO deben forzar selección de empresa
        exempt_paths = [
            "/company/select/",
            "/company/select/clear-flag/",
            "/admin/",
            "/login/",
            "/logout/",
        ]

        if any(request.path.startswith(p) for p in exempt_paths):
            return self.get_response(request)

        # Si el usuario no está autenticado → seguir
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Obtener empresa activa desde la sesión
        company_id = request.session.get("active_company_id")

        if company_id:
            try:
                request.active_company = request.user.companyuser_set.get(
                    company_id=company_id
                ).company
            except CompanyUser.DoesNotExist:
                request.active_company = None
        else:
            request.active_company = None

        # Si no hay empresa activa → redirigir al selector
        if request.active_company is None:
            return redirect(reverse("company:company_select"))

        return self.get_response(request)


# ============================================================
# 🔥 Helper que tus vistas necesitan
# ============================================================

def get_active_company_from_request(request):
    """
    Devuelve la empresa activa asociada al request.
    """
    return getattr(request, "active_company", None)
