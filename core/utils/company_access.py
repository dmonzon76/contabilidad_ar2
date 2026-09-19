# core/utils/company_access.py

from django.core.exceptions import PermissionDenied

def user_has_access(request, company):
    if not request.user.is_authenticated:
        return False
    return request.user.companyuser_set.filter(
        company=company,
        is_active=True,
    ).exists()

def require_company_access(request, company):
    if not user_has_access(request, company):
        raise PermissionDenied("You do not have access to this company.")
