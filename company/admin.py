from django.contrib import admin
from company.models import Company, CompanyProfile, CompanyUser


# -----------------------------
# COMPANY
# -----------------------------
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tax_id",
        "afip_category",
        "city",
        "province",
        "country",
        "zip_code",
        "is_active",
    )
    list_filter = ("afip_category", "is_active", "province", "country")
    search_fields = ("name", "tax_id", "legal_name")
    ordering = ("name",)


# -----------------------------
# COMPANY PROFILE (Tax Profile)
# -----------------------------
@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "vat_21",
        "vat_105",
        "vat_27",
        "vat_exempt",
        "vat_non_taxed",
        "iibb_status",
        "ganancias_status",
        "uses_perceptions",
        "uses_retentions",
    )
    list_filter = (
        "iibb_status",
        "ganancias_status",
        "vat_21",
        "vat_105",
        "vat_27",
        "vat_exempt",
        "vat_non_taxed",
    )
    search_fields = ("company__name", "company__tax_id")
    ordering = ("company",)


# -----------------------------
# COMPANY USERS
# -----------------------------
@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company",
        "role",
        "is_active",
        "can_view_accounting",
        "can_edit_accounting",
        "can_view_fiscal",
        "can_edit_fiscal",
        "can_view_documents",
        "can_edit_documents",
    )
    list_filter = ("role", "is_active", "company")
    search_fields = ("user__username", "company__name")
    ordering = ("company", "user")
