from django.urls import path
from .views.dashboard import sales_dashboard
from .views.invoices import invoice_create, invoice_detail
from .views.customers import (
    customer_list,
    customer_create,
    customer_edit,
    customer_deactivate,
)

app_name = "sales"

urlpatterns = [
    # Dashboard principal de ventas
    path("", sales_dashboard, name="sales_dashboard"),
    # Facturación
    path("invoices/create/", invoice_create, name="invoice_create"),
    path("invoices/<int:invoice_id>/", invoice_detail, name="invoice_detail"),
    # Clientes
    path("customers/", customer_list, name="customer_list"),
    path("customers/add/", customer_create, name="customer_add"),
    path("customers/<int:customer_id>/edit/", customer_edit, name="customer_edit"),
    path(
        "customers/<int:customer_id>/deactivate/",
        customer_deactivate,
        name="customer_deactivate",
    ),
]
