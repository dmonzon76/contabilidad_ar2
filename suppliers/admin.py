from django.contrib import admin
from .models import Supplier

# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "tax_id",
        "email",
        "phone",
        "is_active",
    )

    list_filter = ("company", "is_active")
    search_fields = ("name", "tax_id", "email", "phone")
    ordering = ("name",)
