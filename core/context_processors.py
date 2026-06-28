def active_company(request):
    return {
        "active_company": getattr(request, "active_company", None)
    }
