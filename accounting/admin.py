from django.contrib import admin
from accounting.models import Account
# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "company", "account_type", "is_active")
    list_filter = ("company", "account_type", "is_active")
    search_fields = ("code", "name")
