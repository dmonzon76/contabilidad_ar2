from django.contrib import admin
from .models import InventoryItem, InventoryMovement
# Register your models here.


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "min_stock")
    search_fields = ("product__name",)

@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ("item", "movement_type", "quantity", "date")
    list_filter = ("movement_type",)
