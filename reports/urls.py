from django.urls import path
from reports.views.accounting_dashboard import accounting_dashboard
from reports.views.cc_dashboard import cc_dashboard
from reports.views.inventory_dashboard import inventory_dashboard
from reports.views.purchases_dashboard import purchases_dashboard
from reports.views.sales_dashboard import sales_dashboard

app_name = "reports"

urlpatterns = [
    path("sales/", sales_dashboard, name="sales_dashboard"),
    path("purchases/", purchases_dashboard, name="purchases_dashboard"),
    path("inventory/", inventory_dashboard, name="inventory_dashboard"),
    path("accounting/", accounting_dashboard, name="accounting_dashboard"),
    path("current-accounts/", cc_dashboard, name="cc_dashboard"),
]
