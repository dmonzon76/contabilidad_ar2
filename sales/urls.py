from django.urls import path
from .views.sales import (
    SaleListView,
    SaleCreateView,
    SaleDetailView,
    sale_item_add,
    issue_sale,  # ← 1. Importar la vista
)
from .views.customers import (
    customer_list,
    customer_create,
    customer_tax_edit,
    customer_edit,
)
from .views.dashboard import sales_dashboard

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

    # Customers
    path("customers/", customer_list, name="customer_list"),
    path("customers/new/", customer_create, name="customer_create"),
    path(
        "customers/<int:customer_id>/tax/",
        customer_tax_edit,
        name="customer_tax_edit",
    ),
    path(
        "customers/<int:customer_id>/edit/",
        customer_edit,
        name="customer_edit",
    ),
]