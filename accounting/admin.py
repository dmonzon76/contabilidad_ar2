from django.contrib import admin
from django.utils.html import format_html

from accounting.models import (
    Account,
    AccountMovement,
    JournalEntry,
    JournalEntryLine,
    FiscalYear,
    Period,
    AccountingSettings,
)


# ============================================================
# ACCOUNT
# ============================================================

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = (
        "formatted_name",
        "code",
        "account_type",
        "company",
        "is_active",
    )

    list_filter = (
        "company",
        "account_type",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "company__name",
    )

    ordering = (
        "company",
        "code",
    )

    def formatted_name(self, obj):

        level = getattr(obj, "level", 0)

        indent = "&nbsp;" * (level * 6)

        colors = [
            "#000000",
            "#444444",
            "#666666",
            "#888888",
            "#AAAAAA",
        ]

        color = colors[level] if level < len(colors) else "#CCCCCC"

        return format_html(
            '{}<span style="color:{}; font-weight:{};">{}</span>',
            indent,
            color,
            "bold" if level == 0 else "normal",
            obj.name
        )

    formatted_name.short_description = "Account"


# ============================================================
# FISCAL YEAR
# ============================================================

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):

    list_display = (
        "year",
        "company",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = (
        "company",
        "status",
    )

    search_fields = (
        "company__name",
    )

    ordering = (
        "company",
        "year",
    )


# ============================================================
# PERIOD
# ============================================================

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):

    list_display = (
        "fiscal_year",
        "month",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = (
        "status",
        "fiscal_year__company",
    )

    search_fields = (
        "fiscal_year__year",
    )

    ordering = (
        "fiscal_year__year",
        "month",
    )


# ============================================================
# JOURNAL ENTRY LINES
# ============================================================

class JournalEntryLineInline(admin.TabularInline):

    model = JournalEntryLine
    extra = 0


# ============================================================
# JOURNAL ENTRY
# ============================================================

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "date",
        "company",
        "period",
        "description",
    )

    list_filter = (
        "company",
        "period",
    )

    search_fields = (
        "description",
    )

    ordering = (
        "-date",
        "-id",
    )

    inlines = [
        JournalEntryLineInline,
    ]


# ============================================================
# ACCOUNT MOVEMENTS
# ============================================================

@admin.register(AccountMovement)
class AccountMovementAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "company",
        "origin",
        "date",
        "amount",
        "movement_type",
    )

    list_filter = (
        "company",
        "movement_type",
    )

    search_fields = (
        "description",
    )

    ordering = (
        "-date",
        "-id",
    )

    def origin(self, obj):

        if obj.customer:
            return f"Customer: {obj.customer}"

        if obj.supplier:
            return f"Supplier: {obj.supplier}"

        if obj.sale:
            return f"Sale #{obj.sale.id}"

        if obj.purchase:
            return f"Purchase #{obj.purchase.id}"

        return "-"

    origin.short_description = "Origin"


# ============================================================
# ACCOUNTING SETTINGS
# ============================================================

@admin.register(AccountingSettings)
class AccountingSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "account_customers",
        "account_suppliers",
        "account_sales_goods",
        "account_inventory",
    )

    search_fields = (
        "company__name",
    )

    fieldsets = (

        (
            "Company",
            {
                "fields": (
                    "company",
                )
            }
        ),

        (
            "Sales",
            {
                "fields": (
                    "account_customers",
                    "account_sales_goods",
                    "account_sales_services",
                    "account_iva_debit",
                )
            }
        ),

        (
            "Purchases",
            {
                "fields": (
                    "account_suppliers",
                    "account_expenses",
                    "account_inventory",
                    "account_iva_credit",
                )
            }
        ),

        (
            "Inventory / CMV",
            {
                "fields": (
                    "account_cmv",
                )
            }
        ),

        (
            "Cash and Banks",
            {
                "fields": (
                    "account_cash",
                    "account_bank",
                )
            }
        ),

        (
            "Perceptions",
            {
                "fields": (
                    "account_iva_perception_payable",
                    "account_iibb_perception_payable",
                )
            }
        ),

        (
            "Retentions",
            {
                "fields": (
                    "account_iva_retention_payable",
                    "account_ganancias_retention_payable",
                    "account_iibb_retention_payable",
                )
            }
        ),
    )