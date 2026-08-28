from django.db import models
from company.models import Company
from products.models import Product
from sales.models.sale import Sale
from purchases.models.purchase import Purchase


class Location(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class InventoryItem(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    min_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} @ {self.location.code} — {self.quantity}"


class InventoryMovement(models.Model):
    MOVEMENT_TYPES = (
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, related_name="movements"
    )

    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    # ✔ AHORA SÍ dentro del modelo
    sale = models.ForeignKey(
        Sale,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_movements"
    )

    purchase = models.ForeignKey(
        Purchase,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_movements"
    )

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity} — {self.item.product.name}"
