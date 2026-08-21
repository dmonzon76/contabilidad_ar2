from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("dashboard/", views.inventory_dashboard, name="inventory_dashboard"),

    path("locations/", views.location_list, name="location_list"),
    path("locations/add/", views.location_create, name="location_add"),
    path("locations/<int:pk>/edit/", views.location_edit, name="location_edit"),
    path("locations/<int:pk>/delete/", views.location_delete, name="location_delete"),

    path("movements/", views.movement_list, name="movement_list"),

    path("", views.inventory_list, name="inventory_list"),
    path("add/", views.inventory_add, name="inventory_add"),
    path("<int:pk>/", views.inventory_detail, name="inventory_detail"),
    path("<int:pk>/edit/", views.inventory_edit, name="inventory_edit"),
    path("<int:pk>/delete/", views.inventory_delete, name="inventory_delete"),

    # ⭐ NUEVO: listado de movimientos
    path("movements/", views.movement_list, name="movement_list"),

    path("movement/add/<int:item_id>/", views.movement_add, name="movement_add"),
    path("movement/<int:pk>/edit/", views.movement_edit, name="movement_edit"),
    path("movement/<int:pk>/delete/", views.movement_delete, name="movement_delete"),
]
