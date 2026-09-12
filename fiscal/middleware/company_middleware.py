from django.core.exceptions import PermissionDenied
from company.models import CompanyUser

from company.models import Company, CompanyUser


def get_active_company_from_request(request):
    """
    Helper usado por vistas fiscales y tests.
    Valida:
    - usuario autenticado
    - compañía activa en sesión
    - compañía existente
    - usuario pertenece a la compañía
    """

    # Usuario autenticado
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        raise PermissionDenied("User is not authenticated")

    # Compañía activa en sesión
    company_id = request.session.get("active_company_id")
    if not company_id:
        raise KeyError("No active company selected")

    # Compañía existente
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Company.DoesNotExist("Active company not found")

    # Validar que el usuario pertenece a la compañía
    if not CompanyUser.objects.filter(user=user, company=company, is_active=True).exists():
        raise PermissionDenied("User does not have access to this company")

    return company
