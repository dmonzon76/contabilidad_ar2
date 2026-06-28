# inventory/urls.py

from django.urls import path
from inventory.views import product_list

app_name = "inventory"

urlpatterns = [
    path("products/", product_list, name="product_list"),
]
