import logging
from django.shortcuts import redirect
from company.models import CompanyUser

logger = logging.getLogger(__name__)


class ActiveCompanyMiddleware:
    """
    Garantiza que el usuario autenticado tenga una empresa activa seleccionada
    y valida estrictamente que pertenezca a ella mediante CompanyUser.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Si el usuario no está autenticado → permitir flujo (login/logout)
        if not getattr(request, "user", None) or not request.user.is_authenticated:
            return self.get_response(request)

        # 2. Rutas exentas que no requieren empresa activa
        EXEMPT_PREFIXES = (
            "/admin",
            "/accounts/login/",
            "/accounts/logout/",
            "/static/",
            "/media/",
            "/company/select/",
            "/company/new/",
        )

        if request.path.startswith(EXEMPT_PREFIXES):
            return self.get_response(request)

        # 3. Obtener el ID de empresa activa de la sesión
        active_company_id = request.session.get("active_company_id")

        if not active_company_id:
            logger.debug("No active company — redirecting to company selector")
            request.session["show_company_select_modal"] = True
            return redirect("company:company_select")

        # 4. Validar pertenencia activa en CompanyUser (Aislamiento Multiempresa)
        company_user = (
            CompanyUser.objects.filter(
                user=request.user,
                company_id=active_company_id,
                is_active=True
            )
            .select_related("company")
            .first()
        )

        # Si NO existe la relación CompanyUser → Denegar acceso y redirigir
        if company_user is None:
            logger.warning(
                "Usuario %s intentó acceder a empresa %s sin relación CompanyUser — reseteando.",
                request.user,
                active_company_id,
            )
            request.session.pop("active_company_id", None)
            request.session["show_company_select_modal"] = True
            return redirect("company:company_select")

        # 5. Asignar la empresa validada al request
        request.active_company = company_user.company

        return self.get_response(request)