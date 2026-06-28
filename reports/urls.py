# reports/urls.py

from django.urls import path
from reports.views import report_home

app_name = "reports"

urlpatterns = [
    path("", report_home, name="report_home"),
]
