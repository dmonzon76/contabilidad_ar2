import decimal
from django.core.exceptions import ValidationError
from django.db import models, transaction

from company.models import Company
from fiscal.models.tax import Tax
from products.models import Product
from purchases.models.purchase import Purchase
from sales.models.sale import Sale

class Location(models.Model):
    """
    Ubicación física de almacenamiento vinculada a una empresa.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

class ProductBatch(models.Model):
    """
    Modelo opcional para la trazabilidad de lotes y fechas de vencimiento.
    Permite que empresas del rubro farmacéutico o alimenticio registren vencimientos
    sin forzar el uso de lotes en empresas con inventario simple.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="batches")
    batch_number = models.CharField(max_length=50)
    expiration_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("company", "product", "batch_number")
        verbose_name = "Lote de Producto"
        verbose_name_plural = "Lotes de Productos"

    def __str__(self):
        return f"Lote {self.batch_number} - {self.product.name}"

class InventoryItem(models.Model):
    """
    Representa el stock disponible de un producto en una ubicación específica.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    min_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.product.name} @ {self.location.code} — {self.quantity}"

    def get_current_cost(self):
        """
        Devuelve el último costo de ingreso registrado para este ítem en la ubicación.
        """
        last_in = InventoryMovement.objects.filter(
            item=self, movement_type="IN"
        ).order_by("-date").first()

        if last_in:
            return last_in.unit_cost

        return decimal.Decimal("0.00")

class InventoryMovement(models.Model):
    """
    Registro histórico de entradas (IN) y salidas (OUT) de inventario.
    Actualiza de forma atómica la cantidad en InventoryItem al guardar.
    """
    MOVEMENT_TYPES = (
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )

    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="movements",
    )

    batch = models.ForeignKey(
        ProductBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements",
        help_text="Lote asociado si la empresa requiere trazabilidad de vencimientos.",
    )

    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_TYPES,
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    note = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    date = models.DateTimeField(auto_now_add=True)

    sale = models.ForeignKey(
        Sale,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_movements",
    )

    purchase = models.ForeignKey(
        Purchase,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_movements",
    )

    internal_tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="inventory_movements",
        help_text="Impuesto interno aplicado al producto",
    )

    def __str__(self):
        movement_label = dict(self.MOVEMENT_TYPES).get(
            self.movement_type, self.movement_type
        )
        return f"{movement_label} {self.quantity} — {self.item.product.name}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        self.total_cost = (self.unit_cost * self.quantity).quantize(decimal.Decimal("0.01"))

        with transaction.atomic():
            super().save(*args, **kwargs)

            # Evita duplicar movimientos al editar un registro existente
            if not is_new:
                return

            item = InventoryItem.objects.select_for_update().get(pk=self.item.pk)

            if self.movement_type == "IN":
                item.quantity += self.quantity
            elif self.movement_type == "OUT":
                if item.quantity < self.quantity:
                    raise ValidationError(
                        f"Insufficient stock for {item.product.name}. Available: {item.quantity}"
                    )

                item.quantity -= self.quantity

            item.save(update_fields=["quantity"])

