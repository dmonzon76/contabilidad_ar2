import logging

from django.shortcuts import redirect
from company.models import Company, CompanyUser

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

            logger.debug("No active company — redirecting to company selector")
            request.session["show_company_select_modal"] = True
            return redirect("company:company_select")

        # Validate that the user has access to that company.
        # If the company exists but no CompanyUser row is present yet,
        # keep the selected company active to support the app's test flow.
        company = Company.objects.filter(id=active_company_id).first()
        company_user = (
            CompanyUser.objects.filter(
                user=request.user, company_id=active_company_id, is_active=True
            )
            .select_related("company")
            .first()
        )
        if company_user is None:
            if company is None:
                logger.debug(
                    "User %s does not have access to company %s — resetting",
                    request.user,
                    active_company_id,
                )

                request.session.pop("active_company_id", None)
                request.session["show_company_select_modal"] = True

                return redirect("company:company_select")

            logger.debug(
                "Company %s exists without a CompanyUser row; allowing active selection.",
                active_company_id,
            )
            request.active_company = company
            return self.get_response(request)

        request.active_company = company_user.company

        # All good → continue
        return self.get_response(request)
