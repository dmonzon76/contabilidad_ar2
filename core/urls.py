from django.urls import path
from core.views.dashboard import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("dashboard/", dashboard, name="dashboard"),
]
