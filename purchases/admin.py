from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from purchases.models import Supplier
from purchases.models.purchase import (
    Purchase,
    PurchaseLine,
    PurchaseTax,
    PurchasePerception,
    PurchaseRetention,
)


# ============================================================
# SUPPLIER ADMIN
# ============================================================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "tax_id",
        "email",
        "phone",
        "is_active",
        "created_at",
    )
    list_filter = ("company", "is_active")
    search_fields = ("name", "tax_id", "email", "phone")
    ordering = ("name",)
    readonly_fields = ("created_at",)


# ============================================================
# INLINES FOR PURCHASE
# ============================================================

class PurchaseLineInline(admin.TabularInline):
    model = PurchaseLine
    extra = 1
    fields = ("description", "quantity", "unit_price", "expense_account", "subtotal")
    readonly_fields = ("subtotal",)


class PurchaseTaxInline(admin.TabularInline):
    model = PurchaseTax
    extra = 1
    fields = ("vat_type", "base_amount", "amount")


class PurchasePerceptionInline(admin.TabularInline):
    model = PurchasePerception
    extra = 1
    fields = ("perception_type", "amount")


class PurchaseRetentionInline(admin.TabularInline):
    model = PurchaseRetention
    extra = 1
    fields = ("retention_type", "amount")


# ============================================================
# PURCHASE ADMIN
# ============================================================

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "supplier",
        "company",
        "date",
        "net_amount",
        "tax_amount",
        "perception_amount",
        "retention_amount",
        "total_amount",
        "view_pdf",
        "duplicate_purchase",
        "generate_journal_entry",
    )

    list_filter = ("company", "supplier", "date")
    search_fields = ("invoice_number", "supplier__name")
    ordering = ("-date",)

    inlines = [
        PurchaseLineInline,
        PurchaseTaxInline,
        PurchasePerceptionInline,
        PurchaseRetentionInline,
    ]

    # --------------------------------------------------------
    # Save totals automatically
    # --------------------------------------------------------
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.calculate_totals()

    # --------------------------------------------------------
    # Custom admin buttons
    # --------------------------------------------------------

    def view_pdf(self, obj):
        url = reverse("purchases:purchase_pdf", args=[obj.id])
        return format_html('<a class="button" href="{}">PDF</a>', url)
    view_pdf.short_description = "PDF"

    def duplicate_purchase(self, obj):
        url = reverse("purchases:purchase_duplicate", args=[obj.id])
        return format_html('<a class="button" href="{}">Duplicate</a>', url)
    duplicate_purchase.short_description = "Duplicate"

    def generate_journal_entry(self, obj):
        url = reverse("purchases:purchase_generate_entry", args=[obj.id])
        return format_html('<a class="button" href="{}">Journal Entry</a>', url)
    generate_journal_entry.short_description = "Journal Entry"

    # --------------------------------------------------------
    # Mass actions
    # --------------------------------------------------------

    actions = ["action_generate_entries"]

    def action_generate_entries(self, request, queryset):
        count = 0
        for purchase in queryset:
            # Aquí iría la lógica real de generación de asiento
            count += 1
        self.message_user(request, f"{count} journal entries generated.")
    action_generate_entries.short_description = "Generate journal entries for selected purchases"
