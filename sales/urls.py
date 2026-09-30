from django.urls import path


from .views.dashboard import sales_dashboard
from .views.sales import (
    SaleCreateView,
    SaleDetailView,
    SaleListView,
    issue_sale,  # ← 1. Importar la vista
    sale_item_add,
)

app_name = "sales"

urlpatterns = [
    # Dashboard
    path("dashboard/", sales_dashboard, name="dashboard"),

    # Sales
    path("", SaleListView.as_view(), name="sale_list"),
    path("new/", SaleCreateView.as_view(), name="sale_create"),
    path("<int:pk>/", SaleDetailView.as_view(), name="sale_detail"),
    path("<int:sale_id>/add-item/", sale_item_add, name="sale_item_add"),
    path("<int:pk>/issue/", issue_sale, name="issue_sale"),  # ← 2. Registrar la ruta
]
    