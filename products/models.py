from decimal import Decimal
from django.db import models

from company.models import Company
from accounting.models import Account
from fiscal.models.tax import Tax


class Product(models.Model):
    PRODUCT_TYPES = (
        ("PRODUCT", "Product"),
        ("SERVICE", "Service"),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)

    description = models.CharField(max_length=300, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)

    type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default="PRODUCT")

    income_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products",
    )

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def is_service(self):
        return self.type == "SERVICE"

    @property
    def has_stock(self):
        return self.type == "PRODUCT"

    def get_current_cost(self, location=None):
        from inventory.models import InventoryItem

        if self.is_service:
            return Decimal("0.00")

        if location:
            try:
                item = InventoryItem.objects.get(
                    company=self.company, product=self, location=location
                )
                return item.get_current_cost()
            except InventoryItem.DoesNotExist:
                return Decimal("0.00")

        item = (
            InventoryItem.objects.filter(company=self.company, product=self)
            .order_by("-quantity")
            .first()
        )

        if item:
            return item.get_current_cost()

        return Decimal("0.00")

    def get_inventory_item(self, location):
        from inventory.models import InventoryItem

        item, _ = InventoryItem.objects.get_or_create(
            company=self.company,
            product=self,
            location=location,
            defaults={"quantity": Decimal("0.00")},
        )
        return item
