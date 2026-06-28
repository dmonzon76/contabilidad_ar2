# core/utils/company_access.py

def user_has_access(request, company):
    """
    Verifica que el usuario tenga acceso a la empresa.
    Esto evita que un usuario pueda ver o editar datos de otra empresa
    simplemente cambiando el ID en la URL.
    """
    if not request.user.is_authenticated:
        return False

    return request.user.companyuser_set.filter(company=company).exists()
