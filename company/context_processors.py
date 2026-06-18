from company.models import Company

def active_company(request):
    company_id = request.session.get("active_company_id")
    if company_id:
        try:
            return {"active_company": Company.objects.get(id=company_id)}
        except Company.DoesNotExist:
            pass
    return {"active_company": None}
