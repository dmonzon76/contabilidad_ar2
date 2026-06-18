from django import forms
from accounting.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["code", "name", "parent", "account_type", "is_active"]
    