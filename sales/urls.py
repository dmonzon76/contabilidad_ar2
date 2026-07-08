from django.urls import path
from .views.sales import SaleListView, SaleCreateView, SaleDetailView
from .views.customers import (
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    customer_list,
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
    path("customers/", CustomerListView.as_view(), name="customer_list"),
    path("customers/add/", CustomerCreateView.as_view(), name="customer_add"),
    path("customers/<int:pk>/edit/", CustomerUpdateView.as_view(), name="customer_edit"),
    path("customers/<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer_delete"),
    path("customers/", customer_list, name="customer_list"),
    path("customers/<int:customer_id>/tax/", customer_tax_edit, name="customer_tax_edit"),

]
