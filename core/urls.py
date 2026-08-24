from django.urls import path
from django.shortcuts import redirect
from core.views.dashboard import main_dashboard

def root_redirect(request):
    return redirect("main_dashboard")

urlpatterns = [
    path("", root_redirect, name="root_redirect"),
    path("dashboard/", main_dashboard, name="main_dashboard"),
]
