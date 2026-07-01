from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Sale, SaleItem


# -----------------------------
# Inline para ítems de la venta
# -----------------------------
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ("description", "quantity", "unit_price", "subtotal")
    readonly_fields = ("subtotal",)


# -----------------------------
# Admin de Ventas
# -----------------------------
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "date",
        "customer",
        "company",
        "net_amount",
        "iva_amount",
        "total_amount",
    )
    list_filter = ("company", "customer", "date")
    search_fields = ("number", "customer__name")
    ordering = ("-date", "-number")

    inlines = [SaleItemInline]


# -----------------------------
# Admin de Clientes
# -----------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "tax_id",
        "email",
        "phone",
        "is_active",
        "created_at",
    )
    list_filter = ("company", "is_active")
    search_fields = ("name", "tax_id", "email")
    ordering = ("name",)

    readonly_fields = ("created_at",)
