from django import forms
from fiscal.models.company_profile import CompanyProfile


class CompanyTaxProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            "vat_21",
            "vat_105",
            "vat_27",
            "vat_exempt",
            "vat_non_taxed",
            "iibb_status",
            "ganancias_status",
            "uses_perceptions",
            "uses_retentions",
        ]
