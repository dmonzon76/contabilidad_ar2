from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventory_list, name="inventory_list"),
    path("<int:pk>/", views.inventory_detail, name="inventory_detail"),
    path("movement/add/<int:item_id>/", views.movement_add, name="movement_add"),
]
