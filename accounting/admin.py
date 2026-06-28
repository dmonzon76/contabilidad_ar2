from django.contrib import admin
from django.utils.html import format_html
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("formatted_name", "code", "account_type", "company", "is_active")
    list_filter = ("company", "account_type", "is_active")
    search_fields = ("code", "name", "company__name")
    ordering = ("company", "code")

    def formatted_name(self, obj):
        """Indentación visual según nivel del código."""
        indent = "&nbsp;" * (obj.level * 6)

        colors = ["#000", "#444", "#666", "#888", "#AAA"]
        color = colors[obj.level] if obj.level < len(colors) else "#CCC"

        return format_html(
            f'{indent}<span style="color:{color}; font-weight:{"bold" if obj.level == 0 else "normal"}">'
            f'{obj.name}</span>'
        )

    formatted_name.short_description = "Account"
