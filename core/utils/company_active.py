# core/utils/company_active.py

from company.models import CompanyUser

def get_active_company(request):
    """
    Devuelve la empresa activa seleccionada por el usuario.
    """
    if not request.user.is_authenticated:
        return None

    active_company_id = request.session.get("active_company_id")
    if not active_company_id:
        return None

    try:
        cu = CompanyUser.objects.get(
            user=request.user,
            company_id=active_company_id,
            is_active=True
        )
        return cu.company
    except CompanyUser.DoesNotExist:
        return None

