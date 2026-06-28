from django.urls import path
from purchases.views.supplier import (
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
)
from purchases.views.purchase import (
    PurchaseListView,
    purchase_create,
    purchase_edit,
    PurchaseDetailView,
    purchase_pdf,
    purchase_duplicate,
    purchase_generate_entry,
    purchase_recalculate,
)

app_name = "purchases"

urlpatterns = [
    # Suppliers
    path("suppliers/", SupplierListView.as_view(), name="supplier_list"),
    path("suppliers/new/", SupplierCreateView.as_view(), name="supplier_create"),
    path("suppliers/<int:pk>/edit/", SupplierUpdateView.as_view(), name="supplier_edit"),
    path("suppliers/<int:pk>/delete/", SupplierDeleteView.as_view(), name="supplier_delete"),

    # Purchases
    path("purchases/", PurchaseListView.as_view(), name="purchase_list"),
    path("purchases/new/", purchase_create, name="purchase_create"),
    path("purchases/<int:pk>/edit/", purchase_edit, name="purchase_edit"),
    path("purchases/<int:pk>/detail/", PurchaseDetailView.as_view(), name="purchase_detail"),
    path("purchases/recalculate/", purchase_recalculate, name="purchase_recalculate"),
    
    # Future features (optional)
    path("purchases/<int:pk>/pdf/", purchase_pdf, name="purchase_pdf"),
    path("purchases/<int:pk>/duplicate/", purchase_duplicate, name="purchase_duplicate"),
    path("purchases/<int:pk>/entry/", purchase_generate_entry, name="purchase_generate_entry"),
]
