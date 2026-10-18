from django.contrib import admin

from fiscal.models.tax import Tax
from fiscal.models.tax_jurisdiction import TaxJurisdiction
from fiscal.models.thirdparty_tax_rule import ThirdPartyTaxRule

from .models import (
    AFIPActivity,
    CompanyProfile,
    ElectronicVoucherBook,
    FiscalInvoice,
    FiscalProduct,
    FiscalService,
    TaxRegime,
    ThirdPartyTaxProfile,
)

# =====================================================
# AFIP ACTIVITIES
# =====================================================

admin.site.register(AFIPActivity)


# =====================================================
# COMPANY PROFILE
# =====================================================

admin.site.register(CompanyProfile)


# =====================================================
# THIRD PARTY TAX PROFILE
# =====================================================


@admin.register(ThirdPartyTaxProfile)
class ThirdPartyTaxProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "afip_category",
        "iibb_status",
        "is_active",
    )

    list_filter = (
        "afip_category",
        "iibb_status",
        "is_active",
    )

    search_fields = ("name",)

    ordering = ("name",)


# =====================================================
# TAX JURISDICTIONS
# =====================================================


@admin.register(TaxJurisdiction)
class TaxJurisdictionAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = ("is_active",)

    ordering = ("name",)


# =====================================================
# TAX RULES
# =====================================================


@admin.register(TaxRegime)
class TaxRegimeAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "tax_type",
        "application_type",
        "jurisdiction",
        "rate",
        "minimum_base",
        "account_code",
        "is_active",
    )

    list_filter = (
        "tax_type",
        "application_type",
        "jurisdiction",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering = (
        "tax_type",
        "application_type",
        "name",
    )


# =====================================================
# PROFILE ↔ RULE RELATION
# =====================================================


@admin.register(ThirdPartyTaxRule)
class ThirdPartyTaxRuleAdmin(admin.ModelAdmin):

    list_display = (
        "tax_profile",
        "regime",
        "custom_rate",
        "effective_rate",
        "is_active",
    )

    list_filter = (
        "regime__tax_type",
        "regime__application_type",
        "is_active",
    )

    search_fields = (
        "tax_profile__name",
        "regime__name",
    )


# =====================================================
# ELECTRONIC VOUCHER BOOKS
# =====================================================

admin.site.register(ElectronicVoucherBook)


# =====================================================
# FISCAL INVOICES
# =====================================================


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

    search_fields = (
        "customer_name",
        "number",
        "cae",
        "company__name",
    )

    list_filter = (
        "company",
        "voucher_book",
        "date",
    )


# =====================================================
# FISCAL PRODUCTS
# =====================================================

admin.site.register(FiscalProduct)


# =====================================================
# FISCAL SERVICES
# =====================================================

admin.site.register(FiscalService)


# =====================================================
# TAXES
# =====================================================


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

    list_filter = (
        "is_vat",
        "is_exempt",
        "is_non_taxed",
        "enabled",
    )

    search_fields = (
        "code",
        "name",
    )
