from django.contrib import admin
from .models import (
    AFIPActivity,
    ThirdPartyTaxProfile,
    CompanyProfile,
    ElectronicVoucherBook,
    FiscalInvoice,
    FiscalProduct,
    FiscalService,
)
from fiscal.models.tax import Tax

# AFIP Activities
admin.site.register(AFIPActivity)

# Company Tax Profile
admin.site.register(CompanyProfile)

# Third Party Tax Profiles
admin.site.register(ThirdPartyTaxProfile)

# Electronic Voucher Books (configuración interna)
admin.site.register(ElectronicVoucherBook)


# Fiscal Invoice (nuevo flujo)
@admin.register(FiscalInvoice)
class FiscalInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "company",
        "voucher_book",
        "number",
        "customer_name",
        "total_amount",
        "cae",
    )
    search_fields = ("customer_name", "number", "cae", "company__name")
    list_filter = ("company", "voucher_book", "date")


# Fiscal Products
admin.site.register(FiscalProduct)

# Fiscal Services
admin.site.register(FiscalService)


# Taxes used by purchases and fiscal documents
@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "rate",
        "is_vat",
        "is_exempt",
        "is_non_taxed",
        "enabled",
    )
    list_filter = ("is_vat", "is_exempt", "is_non_taxed", "enabled")
    search_fields = ("code", "name")
