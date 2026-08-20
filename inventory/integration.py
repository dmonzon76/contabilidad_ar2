from inventory.models import InventoryItem, InventoryMovement, Location


def get_default_location(company):
    """
    Devuelve la primera ubicación de la empresa.
    Si no existe, no se puede registrar stock.
    """
    return Location.objects.filter(company=company).first()


# ============================================================
# INTEGRACIÓN CON PURCHASES (ENTRADAS DE STOCK)
# ============================================================

def update_inventory_from_purchase(purchase):
    """
    Aumenta stock automáticamente cuando se registra una compra.
    Cada línea de compra genera un movimiento IN.
    """

    company = purchase.company
    location = get_default_location(company)

    if not location:
        # Si no hay ubicación, no podemos registrar stock
        return

    for line in purchase.lines.all():

        # 1) Obtener o crear el item de inventario
        item, created = InventoryItem.objects.get_or_create(
            company=company,
            product=line.product,
            location=location,
            defaults={"quantity": 0, "min_stock": 0},
        )

        # 2) Crear movimiento IN
        InventoryMovement.objects.create(
            company=company,
            item=item,
            movement_type="IN",
            quantity=line.quantity,
            note=f"Purchase {purchase.invoice_number}",
        )

        # 3) Actualizar stock
        item.quantity += line.quantity
        item.save()


# ============================================================
# INTEGRACIÓN CON SALES (SALIDAS DE STOCK)
# ============================================================

def update_inventory_from_sale(sale):
    """
    Descuenta stock automáticamente cuando se registra una venta.
    Cada SaleItem genera un movimiento OUT.
    Además, asigna el costo real al SaleItem (CMV).
    """

    company = sale.company
    location = get_default_location(company)

    if not location:
        return

    for s_item in sale.items.all():

        # 1) Buscar el item de inventario
        inv_item = InventoryItem.objects.get(
            company=company,
            product=s_item.product,
            location=location,
        )

        # 2) Registrar movimiento OUT
        InventoryMovement.objects.create(
            company=company,
            item=inv_item,
            movement_type="OUT",
            quantity=s_item.quantity,
            note=f"Sale {sale.number}",
        )

        # 3) Actualizar stock
        inv_item.quantity -= s_item.quantity
        inv_item.save()

        # 4) Registrar costo real para CMV
        #    (si tu inventario tiene costo promedio, FIFO, etc., aquí se ajusta)
        s_item.unit_cost = inv_item.product_cost if hasattr(inv_item, "product_cost") else 0
        s_item.cost_subtotal = s_item.unit_cost * s_item.quantity
        s_item.save()

    # 5) Recalcular totales de la venta (incluye CMV)
    sale.recalc_totals()
