from django.urls import path
from core.views.dashboard import dashboard, home

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
]
