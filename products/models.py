from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from accounting.models import Account
from company.models import Company
from fiscal.models.tax import Tax


class Product(models.Model):
    """
    Inventory Item

    Types:
    - PRODUCT : Stock Product
    - SERVICE : Service
    """

    PRODUCT_TYPES = (
        ("PRODUCT", "Stock Product"),
        ("SERVICE", "Service"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products",
    )

    name = models.CharField(
        max_length=150,
    )

    sku = models.CharField(
        max_length=50,
        db_index=True,
    )

    description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    detail = models.TextField(
        blank=True,
        null=True,
    )

    type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPES,
    )

    income_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Revenue Account",
    )

    purchase_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Purchase Account",
    )

    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products",
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "sku"],
                name="unique_product_sku_per_company",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    # =====================================================
    # BUSINESS RULES
    # =====================================================

    @property
    def is_service(self):
        return self.type == "SERVICE"

    @property
    def is_stock_product(self):
        return self.type == "PRODUCT"

    @property
    def manages_inventory(self):
        return self.type == "PRODUCT"

    @property
    def has_stock(self):
        return self.type == "PRODUCT"

    # =====================================================
    # COSTING
    # =====================================================

    def get_current_cost(self, location=None):

        if self.is_service:
            return Decimal("0.00")

        from inventory.models import InventoryItem

        if location:
            try:
                item = InventoryItem.objects.get(
                    company=self.company,
                    product=self,
                    location=location,
                )
                return item.get_current_cost()

            except InventoryItem.DoesNotExist:
                return Decimal("0.00")

        item = (
            InventoryItem.objects.filter(
                company=self.company,
                product=self,
            )
            .order_by("-quantity")
            .first()
        )

        if item:
            return item.get_current_cost()

        return Decimal("0.00")

    # =====================================================
    # INVENTORY
    # =====================================================

    def get_inventory_item(self, location):

        if self.is_service:
            raise ValidationError("Services cannot have inventory items.")

        from inventory.models import InventoryItem

        item, _ = InventoryItem.objects.get_or_create(
            company=self.company,
            product=self,
            location=location,
            defaults={"quantity": Decimal("0.00")},
        )

        return item
