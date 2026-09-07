from decimal import Decimal
from django.db import models

from .sale import Sale
from products.models import Product
from fiscal.models.tax import Tax
from inventory.models import InventoryItem, InventoryMovement, Location


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items",
        null=True,
        blank=True,
    )

    description = models.CharField(max_length=200)

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost_subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sale_items",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.description} ({self.quantity} × {self.unit_price})"

    def save(self, *args, **kwargs):
        # Subtotal comercial
        self.subtotal = self.quantity * self.unit_price

        if self.product:
            # Costo actual desde inventario / producto
            try:
                cost = self.product.get_current_cost()
            except AttributeError:
                cost = Decimal("0.00")

            self.unit_cost = cost
            self.cost_subtotal = self.quantity * self.unit_cost

            # Movimiento de stock solo si NO es servicio
            if self.product.has_stock:
                # Ubicación por defecto: primer depósito de la compañía
                location = (
                    Location.objects.filter(company=self.sale.company)
                    .order_by("id")
                    .first()
                )
                if location is None:
                    raise ValueError(
                        f"No hay Location definida para la compañía {self.sale.company}."
                    )

                # Obtener / crear el item de inventario
                item, _ = InventoryItem.objects.get_or_create(
                    company=self.sale.company,
                    product=self.product,
                    location=location,
                    defaults={"quantity": Decimal("0.00")},
                )

                # Registrar movimiento de stock OUT
                InventoryMovement.objects.create(
                    company=self.sale.company,
                    item=item,
                    movement_type="OUT",
                    quantity=self.quantity,
                    unit_cost=self.unit_cost,
                    sale=self.sale,
                    note=f"Sale {self.sale.number}",
                )

        super().save(*args, **kwargs)

    @property
    def tax_amount(self):
        if not self.tax:
            return Decimal("0.00")
        return self.subtotal * (self.tax.rate / Decimal("100"))
