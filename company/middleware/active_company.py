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

        # If user is not logged in → do nothing
        logger.debug(
            "ActiveCompanyMiddleware start: path=%s user=%s authenticated=%s sessionid=%s session_key=%s cookies=%s",
            request.path,
            getattr(request, "user", None),
            getattr(request.user, "is_authenticated", False),
            request.COOKIES.get("sessionid"),
            request.session.session_key,
            dict(request.COOKIES),
        )

        if not request.user.is_authenticated:
            logger.debug(
                "User not authenticated — skipping active company check; sessionid=%s session_key=%s",
                request.COOKIES.get("sessionid"),
                request.session.session_key,
            )
            return self.get_response(request)

        # Paths that must NOT be blocked
        EXEMPT_PATHS = [
            "/admin",
            "/accounts/login/",
            "/accounts/logout/",
            "/static",
            "/media",
            "/company/select/",
        ]

        # Allow admin, login, logout, static, media, selector
        if any(request.path.startswith(p) for p in EXEMPT_PATHS):
            logger.debug("Request path is exempt: %s", request.path)
            return self.get_response(request)

        # Check active company
        active_company_id = request.session.get("active_company_id")

        # If no company selected → set flag to show selector modal on dashboard
        if not active_company_id:
            logger.debug(
                "No active_company_id in session — setting modal flag and redirecting to dashboard"
            )
            request.session["show_company_select_modal"] = True
            # If we're already on dashboard, allow the view to render (avoid redirect loop)
            try:
                dashboard_path = reverse("dashboard")
            except Exception:
                dashboard_path = "/dashboard/"

            if request.path == dashboard_path:
                return self.get_response(request)

            return redirect("dashboard")

        # Validate that the user has access to that company
        if not CompanyUser.objects.filter(
            user=request.user, company_id=active_company_id, is_active=True
        ).exists():
            # Remove invalid company from session
            logger.debug(
                "Active company id %s not accessible by user %s — removing and redirecting",
                active_company_id,
                request.user,
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

        # All good → continue
        return self.get_response(request)
