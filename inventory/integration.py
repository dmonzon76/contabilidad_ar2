from django.core.exceptions import ValidationError

from inventory.models import InventoryItem, InventoryMovement, Location


def get_default_location(company):
    return Location.objects.filter(company=company).first()

def validate_inventory_before_issue(sale):
    """
    Valida inventario antes de emitir una venta.

    Reglas:
    - Los servicios no validan stock.
    - Los productos físicos deben existir en inventario.
    - Debe existir una ubicación para la empresa.
    - Debe existir stock suficiente.
    """

    company = sale.company

    stock_items = [item for item in sale.items.all() if not item.product.is_service]

    # Venta sólo de servicios
    if not stock_items:
        return

    location = get_default_location(company)

    if not location:
        raise ValidationError("Cannot issue document. No inventory location configured for this company.")

    for sale_item in stock_items:
        try:
            inventory_item = InventoryItem.objects.get(
                company=company,
                product=sale_item.product,
                location=location,
            )

        except InventoryItem.DoesNotExist:
            raise ValidationError(
                f'Cannot issue document. Product "{sale_item.product.name}" is not registered in inventory.'
            )

        if inventory_item.quantity < sale_item.quantity:
            raise ValidationError(
                f'Cannot issue document. Insufficient stock for product "{sale_item.product.name}". '
                f"Available: {inventory_item.quantity}. "
                f"Required: {sale_item.quantity}."
            )
# ============================================================
# ENTRADAS DE STOCK (COMPRAS)
# ============================================================


def update_inventory_from_purchase(purchase):
    company = purchase.company
    location = get_default_location(company)

    if not location:
        return

    for line in purchase.lines.all():
        product = getattr(line, "product", None)
        if product is None:
            continue

        item, created = InventoryItem.objects.get_or_create(
            company=company,
            product=product,
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

def validate_inventory_before_issue(sale):
    """
    Valida inventario antes de emitir una venta.
    """

    company = sale.company

    stock_items = [
        item
        for item in sale.items.all()
        if not item.product.is_service
    ]

    # Venta únicamente de servicios
    if not stock_items:
        return

    location = get_default_location(company)

    if not location:
        raise ValidationError(
            "Cannot issue document. No inventory location configured for this company."
        )

    for sale_item in stock_items:

        try:
            inventory_item = InventoryItem.objects.get(
                company=company,
                product=sale_item.product,
                location=location,
            )

        except InventoryItem.DoesNotExist:

            raise ValidationError(
                f'Cannot issue document. Product "{sale_item.product.name}" is not registered in inventory.'
            )

        if inventory_item.quantity < sale_item.quantity:

            raise ValidationError(
                f'Cannot issue document. '
                f'Insufficient stock for product "{sale_item.product.name}". '
                f'Available: {inventory_item.quantity}. '
                f'Required: {sale_item.quantity}.'
            )

# ============================================================
# SALIDAS DE STOCK (VENTAS)
# ============================================================
def update_inventory_from_sale(sale):
    company = sale.company
    location = get_default_location(company)

    if not location:
        return

    for s_item in sale.items.all():
        if getattr(s_item.product, "is_service", False):
            continue

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

        s_item.save()

    sale.recalc_totals()





# ============================================================
# REVERSIÓN DE VENTAS
# ============================================================


def revert_inventory_from_sale(sale):
    company = sale.company

    movements = InventoryMovement.objects.filter(company=company, sale=sale, movement_type="OUT")

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

    movements = InventoryMovement.objects.filter(company=company, purchase=purchase, movement_type="IN")

    for mv in movements:
        item = mv.item
        item.quantity -= mv.quantity
        item.save()

    movements.delete()
