from django.shortcuts import render
from inventory.integration import update_inventory_from_purchase

# Create your views here.


def purchase_create(request):
    ...
    purchase.calculate_totals()
    update_inventory_from_purchase(purchase)
    ...
