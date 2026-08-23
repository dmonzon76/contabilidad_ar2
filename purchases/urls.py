from django.urls import path

from purchases.views.purchase import (
    PurchaseListView,
    PurchaseDetailView,
    PurchaseCreateView,
    PurchaseUpdateView,
    PurchaseDeleteView,
    purchase_recalculate,
)

from purchases.views.supplier import (
    supplier_list,
    supplier_create,
    supplier_edit,
    supplier_tax_edit,
)

app_name = "purchases"

urlpatterns = [
    # Purchases
    path("", PurchaseListView.as_view(), name="purchase_list"),
    path("<int:pk>/", PurchaseDetailView.as_view(), name="purchase_detail"),
    path("new/", PurchaseCreateView.as_view(), name="purchase_create"),
    path("<int:pk>/edit/", PurchaseUpdateView.as_view(), name="purchase_edit"),
    path("<int:pk>/delete/", PurchaseDeleteView.as_view(), name="purchase_delete"),
    path("recalculate/", purchase_recalculate, name="purchase_recalculate"),

    # Suppliers
    path("suppliers/", supplier_list, name="supplier_list"),
    path("suppliers/new/", supplier_create, name="supplier_create"),
    path("suppliers/<int:supplier_id>/edit/", supplier_edit, name="supplier_edit"),
    path(
        "suppliers/<int:supplier_id>/tax/",
        supplier_tax_edit,
        name="supplier_tax_edit",
    ),
]
