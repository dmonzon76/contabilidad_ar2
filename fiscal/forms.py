from django import forms
from fiscal.models import AFIPActivity, ThirdPartyTaxProfile, CompanyProfile


# ---------------------------------------------------------
# AFIP Activity Form
# ---------------------------------------------------------
class AFIPActivityForm(forms.ModelForm):
    class Meta:
        model = AFIPActivity
        fields = ["code", "description"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }


# ---------------------------------------------------------
# Third Party Tax Profile Form
# ---------------------------------------------------------
class ThirdPartyTaxProfileForm(forms.ModelForm):
    class Meta:
        model = ThirdPartyTaxProfile
        fields = [
            "company",
            "afip_category",
            "iibb_status",
            "ganancias_status",
            "uses_perceptions",
            "uses_retentions",
        ]
        widgets = {
            "company": forms.Select(attrs={"class": "form-control"}),
            "afip_category": forms.Select(attrs={"class": "form-control"}),
            "iibb_status": forms.Select(attrs={"class": "form-control"}),
            "ganancias_status": forms.Select(attrs={"class": "form-control"}),
            "uses_perceptions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "uses_retentions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


# ---------------------------------------------------------
# Company Tax Profile Form
# ---------------------------------------------------------
class CompanyProfileForm(forms.ModelForm):
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
        widgets = {
            "vat_21": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_105": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_27": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_exempt": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_non_taxed": forms.CheckboxInput(attrs={"class": "form-check-input"}),

            "iibb_status": forms.Select(attrs={"class": "form-control"}),
            "ganancias_status": forms.Select(attrs={"class": "form-control"}),

            "uses_perceptions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "uses_retentions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
