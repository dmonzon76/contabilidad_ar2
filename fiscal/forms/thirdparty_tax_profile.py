from django import forms
from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile

class ThirdPartyTaxProfileForm(forms.ModelForm):
    class Meta:
        model = ThirdPartyTaxProfile
        fields = [
            "afip_category",
            "vat_21",
            "vat_105",
            "vat_27",
            "vat_exempt",
            "vat_non_taxed",
            "ganancias_status",
            "iibb_status",
            "uses_perceptions",
            "uses_retentions",
        ]
