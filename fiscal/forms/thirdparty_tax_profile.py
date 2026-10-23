from django import forms

from fiscal.models import ThirdPartyTaxProfile


class ThirdPartyTaxProfileForm(forms.ModelForm):

    class Meta:
        model = ThirdPartyTaxProfile

        fields = [
            "name",
            "afip_category",
            "iibb_status",
            "has_multilateral_agreement",
            "multilateral_number",
            "notes",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "afip_category": forms.Select(
                attrs={"class": "form-select"}
            ),
            "iibb_status": forms.Select(
                attrs={"class": "form-select"}
            ),
            "has_multilateral_agreement": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "multilateral_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        has_cm = cleaned_data.get(
            "has_multilateral_agreement"
        )

        cm_number = cleaned_data.get(
            "multilateral_number"
        )

        iibb_status = cleaned_data.get(
            "iibb_status"
        )

        if has_cm and not cm_number:
            self.add_error(
                "multilateral_number",
                "CM Number is required for multilateral taxpayers.",
            )

        if iibb_status == "MULTILATERAL":
            cleaned_data[
                "has_multilateral_agreement"
            ] = True

        return cleaned_data