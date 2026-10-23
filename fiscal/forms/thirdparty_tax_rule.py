from django import forms

from fiscal.models import ThirdPartyTaxRule


class ThirdPartyTaxRuleForm(forms.ModelForm):

    class Meta:
        model = ThirdPartyTaxRule

        fields = [
            "tax_profile",
            "regime",
            "custom_rate",
            "is_active",
            "notes",
        ]

        widgets = {
            "tax_profile": forms.Select(
                attrs={"class": "form-select"}
            ),
            "regime": forms.Select(
                attrs={"class": "form-select"}
            ),
            "custom_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.0001",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }
