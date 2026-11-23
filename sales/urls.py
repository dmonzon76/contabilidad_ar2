from django.urls import path

from .views.dashboard import sales_dashboard
from .views.sales import (
    SaleCreateView,
    SaleDetailView,
    SaleListView,
    SaleWorkspaceView,
    issue_sale,
    sale_item_add,
    sale_item_delete,
    sale_item_edit,  # NUEVO
)

APP_NAME = "sales"



urlpatterns = [
    
    path("dashboard/", sales_dashboard, name="dashboard"),

    path("", SaleListView.as_view(), name="sale_list"),

    path("new/", SaleCreateView.as_view(), name="sale_create"),

    path("<int:pk>/", SaleDetailView.as_view(), name="sale_detail"),

    path(
        "<int:pk>/workspace/",
        SaleWorkspaceView.as_view(),
        name="sale_workspace",
    ),

    path(
        "<int:sale_id>/add-item/",
        sale_item_add,
        name="sale_item_add",
    ),

    path(
        "item/<int:pk>/delete/",
        sale_item_delete,
        name="sale_item_delete",
    ),

    path(
        "<int:pk>/issue/",
        issue_sale,
        name="issue_sale",
    ),
    path(
    "item/<int:pk>/edit/",
    sale_item_edit,
    name="sale_item_edit",
),
]