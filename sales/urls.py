from django.urls import path
from .views.sales import SaleListView, SaleCreateView, SaleDetailView
from .views.customers import (
    customer_list,
    customer_create,
    customer_edit,
    customer_delete,
    customer_tax_edit,
)
from .views.sales import SaleListView, SaleCreateView, SaleDetailView, sale_item_add

app_name = "sales"

urlpatterns = [
    # Sales
    path("sales/", SaleListView.as_view(), name="sale_list"),
    path("sales/new/", SaleCreateView.as_view(), name="sale_create"),
    path("sales/<int:pk>/", SaleDetailView.as_view(), name="sale_detail"),
    path("sales/<int:sale_id>/items/add/", sale_item_add, name="sale_item_add"),
    # Customers
    path("customers/", customer_list, name="customer_list"),
    path("customers/add/", customer_create, name="customer_add"),
    path("customers/<int:customer_id>/edit/", customer_edit, name="customer_edit"),
    path(
        "customers/<int:customer_id>/delete/", customer_delete, name="customer_delete"
    ),
    path(
        "customers/<int:customer_id>/tax/", customer_tax_edit, name="customer_tax_edit"
    ),
]
