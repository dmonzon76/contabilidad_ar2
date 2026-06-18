from django.shortcuts import render

def error_403(request, exception=None):
    return render(request, "core/errors/403.html", status=403)
