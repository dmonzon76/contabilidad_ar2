from django.urls import path

from purchases.views.purchase import (
    PurchaseListView,
    PurchaseDetailView,
    PurchaseCreateView,
    PurchaseUpdateView,
    PurchaseDeleteView,
)

from purchases.views.supplier import (
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
)

app_name = "purchases"



urlpatterns = [
    # Purchases
    path("", PurchaseListView.as_view(), name="purchase_list"),
    path("<int:pk>/", PurchaseDetailView.as_view(), name="purchase_detail"),
    path("new/", PurchaseCreateView.as_view(), name="purchase_create"),
    path("<int:pk>/edit/", PurchaseUpdateView.as_view(), name="purchase_edit"),
    path("<int:pk>/delete/", PurchaseDeleteView.as_view(), name="purchase_delete"),

    # Suppliers
    path("suppliers/", SupplierListView.as_view(), name="supplier_list"),
    path("suppliers/new/", SupplierCreateView.as_view(), name="supplier_create"),
    path("suppliers/<int:pk>/edit/", SupplierUpdateView.as_view(), name="supplier_edit"),
]

















