from datetime import date
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404, redirect

from .forms import InventoryItemForm, InventoryMovementForm, LocationForm
from .models import InventoryItem, InventoryMovement, Location


# ============================
# Locations
# ============================

def location_list(request):
    company = request.user.active_company
    locations = Location.objects.filter(company=company).order_by("code")
    return render(request, "inventory/location_list.html", {"locations": locations})


def location_create(request):
    company = request.user.active_company

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            loc = form.save(commit=False)
            loc.company = company
            loc.save()
            return redirect("inventory:location_list")
    else:
        form = LocationForm()

    return render(request, "inventory/location_form.html", {"form": form})


def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect("inventory:location_list")
    else:
        form = LocationForm(instance=location)

    return render(request, "inventory/location_form.html", {"form": form})


def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == "POST":
        location.delete()
        return redirect("inventory:location_list")

    return render(request, "inventory/location_delete.html", {"location": location})


# ============================
# Inventory Items
# ============================

def inventory_list(request):
    company = request.user.active_company
    items = InventoryItem.objects.filter(company=company).select_related("product", "location")
    return render(request, "inventory/inventory_list.html", {"items": items})


def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    movements = item.movements.order_by("-date")
    return render(request, "inventory/inventory_detail.html", {"item": item, "movements": movements})


def inventory_add(request):
    company = request.user.active_company

    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = company
            item.save()
            return redirect("inventory:inventory_list")
    else:
        form = InventoryItemForm()

    return render(request, "inventory/inventory_item_form.html", {"form": form})


def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:inventory_detail", pk=pk)
    else:
        form = InventoryItemForm(instance=item)

    return render(request, "inventory/inventory_item_form.html", {"form": form})


def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        item.delete()
        return redirect("inventory:inventory_list")

    return render(request, "inventory/inventory_delete.html", {"item": item})


# ============================
# Movements
# ============================

def movement_add(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)

    if request.method == "POST":
        form = InventoryMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.company = item.company
            movement.item = item
            movement.save()

            if movement.movement_type == "IN":
                item.quantity += movement.quantity
            else:
                item.quantity -= movement.quantity

            item.save()

            return redirect("inventory:inventory_detail", pk=item_id)
    else:
        form = InventoryMovementForm()

    return render(request, "inventory/movement_add.html", {"item": item, "form": form})


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
        if movement.movement_type == "IN":
            item.quantity -= movement.quantity
        else:
            item.quantity += movement.quantity

        item.save()
        movement.delete()

        return redirect("inventory:inventory_detail", pk=item.pk)

    return render(request, "inventory/movement_delete.html", {"movement": movement})


# ============================
# Dashboard
# ============================

def inventory_dashboard(request):
    company = request.user.active_company
    today = date.today()

    items = InventoryItem.objects.filter(company=company)

    total_stock = items.aggregate(total=Sum("quantity"))["total"] or 0
    low_stock = items.filter(quantity__lt=F("min_stock")).count()
    critical_stock = items.filter(quantity=0).count()

    movements_month = InventoryMovement.objects.filter(
        company=company,
        date__year=today.year,
        date__month=today.month,
    ).count()

    context = {
        "total_stock": total_stock,
        "low_stock": low_stock,
        "critical_stock": critical_stock,
        "movements_month": movements_month,
    }

    return render(request, "inventory/dashboard.html", context)
