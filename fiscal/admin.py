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
        "customer",
        "voucher_type",
        "point_of_sale",
        "voucher_number",
        "total",
        "cae",
    )
    search_fields = ("customer__name", "voucher_number", "cae")
    list_filter = ("voucher_type", "point_of_sale", "date")

# Fiscal Products
admin.site.register(FiscalProduct)

# Fiscal Services
admin.site.register(FiscalService)
