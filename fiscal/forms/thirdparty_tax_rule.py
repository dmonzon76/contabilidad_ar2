from django import forms

from fiscal.models import ThirdPartyTaxRule


class ThirdPartyTaxRuleForm(forms.ModelForm):

    class Meta:

        model = ThirdPartyTaxRule

        fields = [
            "regime",
            "calculation_method",
            "custom_rate",
            "is_active",
            "notes",
    ]


        widgets = {

            "regime": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "calculation_method": forms.Select(
                attrs={
            "class": "form-select",
            }
            ),

            "custom_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.0001",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }