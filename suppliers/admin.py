from django.contrib import admin

from .models import Supplier

# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "tax_profile",
        "email",
        "phone",
        "address",
    )

    list_filter = ("company",)
    search_fields = ("name", "tax_profile", "email", "phone")
    ordering = ("name",)
