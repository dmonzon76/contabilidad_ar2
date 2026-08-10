from datetime import date

from django.db import models
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from .forms import InventoryItemForm, InventoryMovementForm, LocationForm
from .models import InventoryItem, InventoryMovement, Location


# ============================
# Locations (CRUD)
# ============================

def location_list(request):
    locations = Location.objects.all().order_by("code")
    return render(request, "inventory/location_list.html", {"locations": locations})


def location_create(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:location_list")
    else:
        form = LocationForm()

    return render(request, "inventory/location_form.html", {
        "form": form,
        "title": "Create Location"
    })


def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect("inventory:location_list")
    else:
        form = LocationForm(instance=location)

    return render(request, "inventory/location_form.html", {
        "form": form,
        "title": "Edit Location"
    })


def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == "POST":
        location.delete()
        return redirect("inventory:location_list")

    return render(request, "inventory/location_delete.html", {"location": location})


# ============================
# Inventory Items (CRUD)
# ============================

def inventory_list(request):
    items = InventoryItem.objects.select_related("product", "location").all()
    return render(request, "inventory/inventory_list.html", {"items": items})


def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    movements = item.movements.order_by("-date")
    return render(request, "inventory/inventory_detail.html", {
        "item": item,
        "movements": movements
    })


def inventory_add(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:inventory_list")
    else:
        form = InventoryItemForm()

    return render(request, "inventory/inventory_item_form.html", {
        "form": form,
        "title": "Create Inventory Item"
    })


def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:inventory_detail", pk=pk)
    else:
        form = InventoryItemForm(instance=item)

    return render(request, "inventory/inventory_item_form.html", {
        "form": form,
        "title": "Edit Inventory Item"
    })


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
        form = InventoryMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.item = item
            movement.save()

            # actualizar stock
            if movement.movement_type == "IN":
                item.quantity += movement.quantity
            else:
                item.quantity -= movement.quantity

            item.save()

            return redirect("inventory:inventory_detail", pk=item_id)
    else:
        form = InventoryMovementForm()

    return render(request, "inventory/movement_add.html", {
        "item": item,
        "form": form
    })


def movement_edit(request, pk):
    movement = get_object_or_404(InventoryMovement, pk=pk)
    item = movement.item

    if request.method == "POST":
        old_qty = movement.quantity
        old_type = movement.movement_type

        form = InventoryMovementForm(request.POST, instance=movement)
        if form.is_valid():
            new_movement = form.save(commit=False)

            # revertir movimiento anterior
            if old_type == "IN":
                item.quantity -= old_qty
            else:
                item.quantity += old_qty

            # aplicar movimiento nuevo
            if new_movement.movement_type == "IN":
                item.quantity += new_movement.quantity
            else:
                item.quantity -= new_movement.quantity

            item.save()
            new_movement.save()

            return redirect("inventory:inventory_detail", pk=item.pk)
    else:
        form = InventoryMovementForm(instance=movement)

    return render(request, "inventory/movement_edit.html", {"form": form})


def movement_delete(request, pk):
    movement = get_object_or_404(InventoryMovement, pk=pk)
    item = movement.item

    if request.method == "POST":
        # revertir movimiento
        if movement.movement_type == "IN":
            item.quantity -= movement.quantity
        else:
            item.quantity += movement.quantity

        item.save()
        movement.delete()

        return redirect("inventory:inventory_detail", pk=item.pk)

    return render(request, "inventory/movement_delete.html", {"movement": movement})


# ============================
# Inventory Dashboard (KPIs + Charts)
# ============================

def inventory_dashboard(request):
    today = date.today()
    month = today.month
    year = today.year

    items = InventoryItem.objects.select_related("product", "location").all()

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

    top_out_labels = [item["item__product__name"] for item in top_out_raw]
    top_out_values = [item["total"] for item in top_out_raw]

    # Datos para gráficos
    stock_labels = [f"{item.product.name} ({item.location.code})" for item in items]
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
