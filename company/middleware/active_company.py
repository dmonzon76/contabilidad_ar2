import logging

from django.shortcuts import redirect
from company.models import CompanyUser
from django.urls import reverse

logger = logging.getLogger(__name__)


class ActiveCompanyMiddleware:
    """
    Ensures the user has an active company selected.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Log info
        logger.debug(
            "ActiveCompanyMiddleware start: path=%s user=%s authenticated=%s",
            request.path,
            getattr(request, "user", None),
            getattr(request.user, "is_authenticated", False),
        )

        # If user is not logged in → allow everything
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Paths that must NOT be blocked
        EXEMPT_PREFIXES = (
            "/admin",  # admin root + all subpaths
            "/accounts/login/",
            "/accounts/logout/",
            "/static/",
            "/media/",
            "/company/select/",
            "/company/new/",
        )

        # Allow admin, login, logout, static, media, selector
        if request.path.startswith(EXEMPT_PREFIXES):
            logger.debug("Request path is exempt: %s", request.path)
            return self.get_response(request)

        # Check active company
        active_company_id = request.session.get("active_company_id")

        # ⭐ FIX: allow admin even if no company is selected
        if not active_company_id:

            # If user is accessing admin → allow without company
            if request.path.startswith("/admin/"):
                logger.debug("Admin access without company allowed.")
                return self.get_response(request)

            logger.debug("No active company — redirecting to dashboard")
            request.session["show_company_select_modal"] = True

            try:
                dashboard_path = reverse("dashboard")
            except Exception:
                dashboard_path = "/dashboard/"

            # Avoid redirect loop
            if request.path == dashboard_path:
                return self.get_response(request)

            return redirect("dashboard")

        # Validate that the user has access to that company
        company_user = (
            CompanyUser.objects.filter(
                user=request.user, company_id=active_company_id, is_active=True
            )
            .select_related("company")
            .first()
        )
        if company_user is None:

            logger.debug(
                "User %s does not have access to company %s — resetting",
                request.user,
                active_company_id,
            )

            request.session.pop("active_company_id", None)
            request.session["show_company_select_modal"] = True

            try:
                dashboard_path = reverse("dashboard")
            except Exception:
                dashboard_path = "/dashboard/"

            if request.path == dashboard_path:
                return self.get_response(request)

            return redirect("dashboard")

        request.active_company = company_user.company

        # All good → continue
        return self.get_response(request)
