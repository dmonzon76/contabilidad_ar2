from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from core.utils.company_active import get_active_company


def company_required(view_func):
    """Require an authenticated user with a valid active company."""

    @login_required
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        company = get_active_company(request)
        if company is None:
            request.session["show_company_select_modal"] = True
            return redirect("company:company_select")

        request.active_company = company
        return view_func(request, *args, **kwargs)

    return wrapped
