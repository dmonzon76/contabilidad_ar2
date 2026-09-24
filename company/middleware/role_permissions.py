import logging
from django.http import HttpResponseForbidden
from django.urls import resolve, Resolver404
from company.models import CompanyUser

logger = logging.getLogger(__name__)


class RolePermissionMiddleware:
    """
    Controla el acceso a módulos y la distinción entre permisos de lectura y escritura.
    """

    # Mapeo de módulos a permisos de Lectura y Escritura
    PERMISSION_MAP = {
        "accounting": {"view": "can_view_accounting", "edit": "can_edit_accounting"},
        "fiscal": {"view": "can_view_fiscal", "edit": "can_edit_fiscal"},
        "documents": {"view": "can_view_documents", "edit": "can_edit_documents"},
        "sales": {"view": "can_view_sales", "edit": "can_edit_sales"},
        "purchases": {"view": "can_view_purchases", "edit": "can_edit_purchases"},
        "inventory": {"view": "can_view_inventory", "edit": "can_edit_inventory"},
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Si no está autenticado o es Superusuario → omitir chequeo
        if not request.user.is_authenticated or request.user.is_superuser:
            return self.get_response(request)

        # 2. Si no hay empresa activa seleccionada → omitir (lo maneja ActiveCompanyMiddleware)
        company_id = request.session.get("active_company_id")
        if not company_id:
            return self.get_response(request)

        # 3. Resolver el app_name de forma segura frente a URLs inexistentes (404)
        try:
            resolver = resolve(request.path)
            app_name = resolver.app_name
        except Resolver404:
            return self.get_response(request)

        if not app_name or app_name not in self.PERMISSION_MAP:
            return self.get_response(request)

        # 4. Validar pertenencia a la empresa
        cu = CompanyUser.objects.filter(
            user=request.user,
            company_id=company_id,
            is_active=True
        ).first()

        if not cu:
            return HttpResponseForbidden("No tenés acceso a esta empresa.")

        # 5. Determinar si la petición es de Lectura (GET, HEAD, OPTIONS) o Modificación (POST, PUT, DELETE)
        is_write_operation = request.method not in ("GET", "HEAD", "OPTIONS")
        perm_type = "edit" if is_write_operation else "view"

        required_perm = self.PERMISSION_MAP[app_name].get(perm_type)

        # Si tiene el atributo de permiso en CompanyUser y está en False → Denegar
        if required_perm and not getattr(cu, required_perm, False):
            logger.warning(
                "Usuario %s intentó operación %s en app '%s' sin permiso '%s'.",
                request.user,
                request.method,
                app_name,
                required_perm,
            )
            return HttpResponseForbidden("No tenés permisos para realizar esta acción en el módulo.")

        return self.get_response(request)
