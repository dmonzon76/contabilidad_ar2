from django.urls import path
from core.views.dashboard import dashboard
from core.views.auth import logout_view

app_name = "core"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("accounts/logout/", logout_view, name="logout"),
]
