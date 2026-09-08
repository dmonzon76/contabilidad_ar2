from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Account,
    AccountMovement,
    JournalEntry,
    JournalEntryLine,
    FiscalYear,
    Period,
)


# ============================================================
# ACCOUNT
# ============================================================

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("formatted_name", "code", "account_type", "company", "is_active")
    list_filter = ("company", "account_type", "is_active")
    search_fields = ("code", "name", "company__name")
    ordering = ("company", "code")

    def formatted_name(self, obj):
        indent = "&nbsp;" * (obj.level * 6)
        colors = ["#000", "#444", "#666", "#888", "#AAA"]
        color = colors[obj.level] if obj.level < len(colors) else "#CCC"
        return format_html(
            f'{indent}<span style="color:{color}; font-weight:{"bold" if obj.level == 0 else "normal"}">'
            f'{obj.name}</span>'
        )

    formatted_name.short_description = "Account"


# ============================================================
# FISCAL YEAR
# ============================================================

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ("year", "company", "start_date", "end_date", "status")
    list_filter = ("company", "status")
    search_fields = ("company__name",)
    ordering = ("company", "year")


# ============================================================
# PERIOD
# ============================================================

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ("fiscal_year", "month", "start_date", "end_date", "status")
    list_filter = ("status", "fiscal_year__company")
    search_fields = ("fiscal_year__year",)
    ordering = ("fiscal_year__year", "month")


# ============================================================
# JOURNAL ENTRY
# ============================================================

class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 0


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "company", "period", "description")
    list_filter = ("company", "period")
    search_fields = ("description",)
    ordering = ("date",)
    inlines = [JournalEntryLineInline]


# ============================================================
# ACCOUNT MOVEMENT
# ============================================================

@admin.register(AccountMovement)
class AccountMovementAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "origin", "date", "amount", "movement_type")
    list_filter = ("company", "movement_type")
    search_fields = ("description",)
    ordering = ("date",)

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
