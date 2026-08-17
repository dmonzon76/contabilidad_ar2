from django.contrib import admin

from .models.thirdparty_tax import ThirdPartyTaxProfile
from .models import (
    ElectronicVoucherBook,
    FiscalInvoice,
    FiscalInvoiceLine,
    FiscalProduct,
    FiscalService,
    FiscalSale,
)

# -----------------------------
# Third Party Tax Profile
# -----------------------------
@admin.register(ThirdPartyTaxProfile)
class ThirdPartyTaxProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "company",
        "afip_category",
        "ganancias_status",
        "iibb_status",
        "uses_perceptions",
        "uses_retentions",
    ]
    list_filter = [
        "afip_category",
        "ganancias_status",
        "iibb_status",
        "uses_perceptions",
        "uses_retentions",
    ]
    search_fields = [
        "company__name",
        "company__tax_id",
    ]

# -----------------------------
# Electronic Voucher Book
# -----------------------------
@admin.register(ElectronicVoucherBook)
class ElectronicVoucherBookAdmin(admin.ModelAdmin):
    list_display = ("voucher_type", "point_of_sale", "current_number", "enabled")
    list_filter = ("voucher_type", "enabled")
    search_fields = ("point_of_sale",)

# -----------------------------
# Fiscal Models
# -----------------------------
@admin.register(FiscalInvoice)
class FiscalInvoiceAdmin(admin.ModelAdmin):
    list_display = ("date", "customer", "voucher_book", "voucher_number", "total")

@admin.register(FiscalInvoiceLine)
class FiscalInvoiceLineAdmin(admin.ModelAdmin):
    list_display = ("invoice", "description", "quantity", "price", "vat_rate")

@admin.register(FiscalProduct)
class FiscalProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "vat_rate")

@admin.register(FiscalService)
class FiscalServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "vat_rate")

@admin.register(FiscalSale)
class FiscalSaleAdmin(admin.ModelAdmin):
    list_display = ("sale", "voucher_book", "invoice")
