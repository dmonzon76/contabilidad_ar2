from django.contrib import admin
from .models.thirdparty_tax import ThirdPartyTaxProfile
from .models import FiscalVoucherBook

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

from .models import ElectronicVoucherBook

@admin.register(ElectronicVoucherBook)
class ElectronicVoucherBookAdmin(admin.ModelAdmin):
    list_display = ('voucher_type', 'point_of_sale', 'current_number', 'enabled')
    list_filter = ('voucher_type', 'enabled')
    search_fields = ('point_of_sale',)
