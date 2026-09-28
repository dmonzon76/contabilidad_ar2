import logging

from django.http import HttpResponseForbidden
from django.urls import Resolver404, resolve

from company.models import CompanyUser

logger = logging.getLogger(__name__)


class RolePermissionMiddleware:
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
        if not request.user.is_authenticated or request.user.is_superuser:
            return self.get_response(request)

        company_id = request.session.get("active_company_id")
        if not company_id:
            return self.get_response(request)

        try:
            resolver = resolve(request.path)
            app_name = resolver.app_name
        except Resolver404:
            return self.get_response(request)

        if not app_name or app_name not in self.PERMISSION_MAP:
            return self.get_response(request)

        cu = CompanyUser.objects.filter(user=request.user, company_id=company_id, is_active=True).first()
        if cu is None:
            return HttpResponseForbidden("No tenés permisos para esta acción.")

        is_write = request.method in ("POST", "PUT", "PATCH", "DELETE")
        required_perm = self.PERMISSION_MAP[app_name].get("edit" if is_write else "view")

        if cu.role in ("OWNER", "ADMIN"):
            if not is_write and required_perm and hasattr(cu, required_perm) and not getattr(cu, required_perm):
                return HttpResponseForbidden("No tenés permisos para esta acción.")
            return self.get_response(request)

        if required_perm and not getattr(cu, required_perm, False):
            return HttpResponseForbidden("No tenés permisos para realizar esta acción en el módulo.")

        return self.get_response(request)
