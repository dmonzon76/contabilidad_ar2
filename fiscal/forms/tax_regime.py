from django import forms

from fiscal.models import TaxRegime


class TaxRegimeForm(forms.ModelForm):

    class Meta:

        model = TaxRegime

        fields = [
            "code",
            "name",
            "tax_type",
            "application_type",
            "tax",
            "jurisdiction",
            "rate",
            "minimum_base",
            "account_code",
            "valid_from",
            "valid_to",
            "is_active",
        ]

        widgets = {

            "code": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "tax_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "application_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "tax": forms.Select(
                attrs={"class": "form-select"}
            ),

            "jurisdiction": forms.Select(
                attrs={"class": "form-select"}
            ),

            "rate": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "minimum_base": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "account_code": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "valid_from": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "valid_to": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }