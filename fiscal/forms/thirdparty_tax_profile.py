from django import forms

from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile


class ThirdPartyTaxProfileForm(forms.ModelForm):

    class Meta:
        model = ThirdPartyTaxProfile

        fields = [
            "company",
            "name",
            "afip_category",
            "iibb_status",
            "is_active",
            "notes",
        ]

        widgets = {
            "company": forms.Select(
                attrs={"class": "form-control"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "afip_category": forms.Select(
                attrs={"class": "form-control"}
            ),
            "iibb_status": forms.Select(
                attrs={"class": "form-control"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }