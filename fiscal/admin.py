from django.contrib import admin
from .models.thirdparty_tax import ThirdPartyTaxProfile


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
