from company.models import Company

class ActiveCompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        company_id = request.session.get("active_company_id")

        request.active_company = None
        request.company = None
        request.current_company = None

        if company_id:
            try:
                company = Company.objects.get(id=company_id)
                request.active_company = company
                request.company = company
                request.current_company = company
            except Company.DoesNotExist:
                request.session["active_company_id"] = None

        response = self.get_response(request)
        return response
