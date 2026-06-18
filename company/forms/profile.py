from django import forms
from company.models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            "vat_21",
            "vat_105",
            "vat_27",
            "vat_exempt",
            "vat_non_taxed",
            "iibb_registered",
            "ganancias_agent",
            "uses_perceptions",
            "uses_retentions",
        ]
