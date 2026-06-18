from django import forms
from company.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "legal_name",
            "tax_id",
            "afip_category",
            "address",
            "city",
            "province",
            "zip_code",
            "country",
            "start_date",
            "accounting_start_date",
        ]

