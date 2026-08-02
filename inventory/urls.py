from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("dashboard/", views.inventory_dashboard, name="inventory_dashboard"),

    # Inventory items
    path("", views.inventory_list, name="inventory_list"),
    path("add/", views.inventory_add, name="inventory_add"),
    path("<int:pk>/", views.inventory_detail, name="inventory_detail"),
    path("<int:pk>/edit/", views.inventory_edit, name="inventory_edit"),
    path("<int:pk>/delete/", views.inventory_delete, name="inventory_delete"),

    # Movements
    path("movement/add/<int:item_id>/", views.movement_add, name="movement_add"),
    path("movement/<int:pk>/edit/", views.movement_edit, name="movement_edit"),
    path("movement/<int:pk>/delete/", views.movement_delete, name="movement_delete"),
]
