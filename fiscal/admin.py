from django.contrib import admin
from fiscal.models import AFIPActivity, ThirdPartyTaxProfile


@admin.register(AFIPActivity)
class AFIPActivityAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code", "description", "description_long")
    ordering = ("code",)


@admin.register(ThirdPartyTaxProfile)
class ThirdPartyTaxProfileAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "afip_category",
        "ganancias_status",
        "iibb_rate",
        "iibb_exempt",
        "perceptions_enabled",
        "retentions_enabled",
    )

    list_filter = (
        "afip_category",
        "ganancias_status",
        "iibb_exempt",
        "perceptions_enabled",
        "retentions_enabled",
    )

    search_fields = (
        "company__name",
        "company__tax_id",
    )

    # Si tu modelo tiene FK a AFIPActivity, activar Select2:
    autocomplete_fields = []

    def __str__(self):
        return f"{self.code} – {self.description}"
