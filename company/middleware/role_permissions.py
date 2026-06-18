from django.http import HttpResponseForbidden
from django.urls import resolve
from company.models import CompanyUser


class RolePermissionMiddleware:
    """
    Enforces permissions based on URL patterns.
    """

    PERMISSION_MAP = {
        "accounting": "can_view_accounting",
        "fiscal": "can_view_fiscal",
        "documents": "can_view_documents",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # If user is not logged in → no permission checks
        if not request.user.is_authenticated:
            return self.get_response(request)

        # If no company selected → skip
        company_id = request.session.get("active_company_id")
        if not company_id:
            return self.get_response(request)

        # Resolve current app name
        resolver = resolve(request.path)
        app_name = resolver.app_name

        # Skip if no app name (dashboard, home, etc.)
        if not app_name:
            return self.get_response(request)

        # Validate that the user belongs to the company
        try:
            cu = CompanyUser.objects.get(
                user=request.user,
                company_id=company_id,
                is_active=True
            )
        except CompanyUser.DoesNotExist:
            return HttpResponseForbidden("You do not belong to this company.")

        # Check permission based on app
        if app_name in self.PERMISSION_MAP:
            perm = self.PERMISSION_MAP[app_name]
            if not getattr(cu, perm, False):
                return HttpResponseForbidden("You do not have permission to access this module.")

        return self.get_response(request)
