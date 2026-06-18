from django.contrib import admin
from company.models import Company, CompanyProfile, CompanyUser, CompanyActivity


# -----------------------------
# COMPANY
# -----------------------------
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "legal_name",
        "tax_id",
        "afip_category",
        "address",
        "city",
        "province",
        "zip_code",
        "country",
        "is_active",
    )
    list_filter = (
        "afip_category",
        "is_active",
        "province",
        "country",
    )
    search_fields = (
        "name",
        "legal_name",
        "tax_id",
    )
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
        "iibb_registered",
        "ganancias_agent",
    )
    list_filter = (
        "vat_21",
        "vat_105",
        "vat_27",
        "iibb_registered",
        "ganancias_agent",
    )
    search_fields = (
        "company__name",
        "company__tax_id",
    )


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
    list_filter = (
        "role",
        "is_active",
        "company",
    )
    search_fields = (
        "user__username",
        "company__name",
    )
    ordering = ("company", "user")


# -----------------------------
# COMPANY ACTIVITIES
# -----------------------------
@admin.register(CompanyActivity)
class CompanyActivityAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "description",
        "company",
        "is_primary",
        "jurisdiction",
    )
    list_filter = (
        "company",
        "is_primary",
    )
    search_fields = (
        "code",
        "description",
        "company__name",
    )
    ordering = ("company", "code")
