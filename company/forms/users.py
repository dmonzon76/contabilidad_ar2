from django import forms
from company.models import CompanyUser


class CompanyUserForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
        fields = [
            "user",
            "role",
            "can_view_accounting",
            "can_edit_accounting",
            "can_view_fiscal",
            "can_edit_fiscal",
            "can_view_documents",
            "can_edit_documents",
            "is_active",
        ]
