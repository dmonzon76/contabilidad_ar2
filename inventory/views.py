from datetime import date

from django.db import models
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from .forms import InventoryItemForm, InventoryMovementForm
from .models import InventoryItem, InventoryMovement


# ============================
# Inventory Items (CRUD)
# ============================

def inventory_list(request):
    items = InventoryItem.objects.select_related("product").all()
    return render(request, "inventory/inventory_list.html", {"items": items})


def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    movements = item.movements.order_by("-date")
    return render(
        request,
        "inventory/inventory_detail.html",
        {"item": item, "movements": movements},
    )


def inventory_add(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:inventory_list")
    else:
        form = InventoryItemForm()

    return render(request, "inventory/inventory_add.html", {"form": form})


def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:inventory_detail", pk=pk)
    else:
        form = InventoryItemForm(instance=item)

    return render(
        request,
        "inventory/inventory_edit.html",
        {"form": form, "item": item},
    )


def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        item.delete()
        return redirect("inventory:inventory_list")

    return render(request, "inventory/inventory_delete.html", {"item": item})


# ============================
# Inventory Movements (CRUD)
# ============================

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
            note=note,
        )

        # actualizar stock
        if movement_type == "IN":
            item.quantity += quantity
        else:
            item.quantity -= quantity

        item.save()

        return redirect("inventory:inventory_detail", pk=item_id)

    return render(request, "inventory/movement_add.html", {"item": item})


def movement_edit(request, pk):
    movement = get_object_or_404(InventoryMovement, pk=pk)

    if request.method == "POST":
        form = InventoryMovementForm(request.POST, instance=movement)
        if form.is_valid():
            form.save()
            return redirect("inventory:inventory_detail", pk=movement.item.pk)
    else:
        form = InventoryMovementForm(instance=movement)

    return render(request, "inventory/movement_edit.html", {"form": form})


def movement_delete(request, pk):
    movement = get_object_or_404(InventoryMovement, pk=pk)
    item_id = movement.item.pk

    if request.method == "POST":
        movement.delete()
        return redirect("inventory:inventory_detail", pk=item_id)

    return render(request, "inventory/movement_delete.html", {"movement": movement})


# ============================
# Inventory Dashboard (KPIs + Charts)
# ============================
def inventory_dashboard(request):
    today = date.today()
    month = today.month
    year = today.year

    items = InventoryItem.objects.select_related("product").all()

    # KPIs
    total_stock = items.aggregate(total=Sum("quantity"))["total"] or 0
    low_stock = items.filter(quantity__lt=models.F("min_stock")).count()
    critical_stock = items.filter(quantity=0).count()

    movements_month = InventoryMovement.objects.filter(
        date__year=year,
        date__month=month,
    ).count()

    # Top 5 productos con más salidas
    top_out_raw = (
        InventoryMovement.objects.filter(movement_type="OUT")
        .values("item__product__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]
    )

    # Convertir datos para Chart.js
    top_out_labels = [item["item__product__name"] for item in top_out_raw]
    top_out_values = [item["total"] for item in top_out_raw]

    # Datos para gráficos
    stock_labels = [item.product.name for item in items]
    stock_values = [item.quantity for item in items]

    movement_labels = list(range(1, 32))
    movement_values = [
        InventoryMovement.objects.filter(
            date__year=year,
            date__month=month,
            date__day=day,
        ).count()
        for day in movement_labels
    ]

    context = {
        "total_stock": total_stock,
        "low_stock": low_stock,
        "critical_stock": critical_stock,
        "movements_month": movements_month,

        "stock_labels": stock_labels,
        "stock_values": stock_values,

        "movement_labels": movement_labels,
        "movement_values": movement_values,

        "top_out_labels": top_out_labels,
        "top_out_values": top_out_values,
    }

    return render(request, "inventory/dashboard.html", context)












































