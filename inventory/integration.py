from inventory.models import InventoryItem, InventoryMovement, Location


def get_default_location(company):
    return Location.objects.filter(company=company).first()


# ============================================================
# ENTRADAS DE STOCK (COMPRAS)
# ============================================================

def update_inventory_from_purchase(purchase):
    company = purchase.company
    location = get_default_location(company)

    if not location:
        return

    for line in purchase.lines.all():

        item, created = InventoryItem.objects.get_or_create(
            company=company,
            product=line.product,
            location=location,
            defaults={"quantity": 0, "min_stock": 0},
        )

        InventoryMovement.objects.create(
            company=company,
            item=item,
            movement_type="IN",
            quantity=line.quantity,
            purchase=purchase,
            note=f"Purchase {purchase.invoice_number}",
        )

        item.quantity += line.quantity
        item.save()


# ============================================================
# SALIDAS DE STOCK (VENTAS)
# ============================================================

def update_inventory_from_sale(sale):
    company = sale.company
    location = get_default_location(company)

    if not location:
        return

    for s_item in sale.items.all():

        inv_item = InventoryItem.objects.get(
            company=company,
            product=s_item.product,
            location=location,
        )

        InventoryMovement.objects.create(
            company=company,
            item=inv_item,
            movement_type="OUT",
            quantity=s_item.quantity,
            sale=sale,
            note=f"Sale {sale.number}",
        )

        inv_item.quantity -= s_item.quantity
        inv_item.save()

        s_item.unit_cost = getattr(inv_item, "product_cost", 0)
        s_item.cost_subtotal = s_item.unit_cost * s_item.quantity
        s_item.save()

    sale.recalc_totals()


# ============================================================
# REVERSIÓN DE VENTAS
# ============================================================

def revert_inventory_from_sale(sale):
    company = sale.company

    movements = InventoryMovement.objects.filter(
        company=company,
        sale=sale,
        movement_type="OUT"
    )

    for mv in movements:
        item = mv.item
        item.quantity += mv.quantity
        item.save()

    movements.delete()


# ============================================================
# REVERSIÓN DE COMPRAS
# ============================================================

def revert_inventory_from_purchase(purchase):
    company = purchase.company

    movements = InventoryMovement.objects.filter(
        company=company,
        purchase=purchase,
        movement_type="IN"
    )

    for mv in movements:
        item = mv.item
        item.quantity -= mv.quantity
        item.save()

    movements.delete()
