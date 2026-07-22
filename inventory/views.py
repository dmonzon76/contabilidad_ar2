from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem, InventoryMovement

def inventory_list(request):
    items = InventoryItem.objects.select_related("product").all()
    return render(request, "inventory/inventory_list.html", {"items": items})


def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    movements = item.movements.order_by("-date")
    return render(request, "inventory/inventory_detail.html", {
        "item": item,
        "movements": movements
    })


def movement_add(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)

    if request.method == "POST":
        movement_type = request.POST.get("movement_type")
        quantity = int(request.POST.get("quantity"))
        note = request.POST.get("note")

        InventoryMovement.objects.create(
            item=item,
            movement_type=movement_type,
            quantity=quantity,
            note=note
        )

        # actualizar stock
        if movement_type == "IN":
            item.quantity += quantity
        else:
            item.quantity -= quantity

        item.save()

        return redirect("inventory_detail", pk=item_id)

    return render(request, "inventory/movement_add.html", {"item": item})
