from django import forms
from company.models import CompanyActivity


class CompanyActivityForm(forms.ModelForm):

    class Meta:
        model = CompanyActivity
        fields = ["activity", "jurisdiction", "is_primary"]

        widgets = {
            "activity": forms.Select(
                attrs={
                    "class": "form-select select2-afip",
                    "data-placeholder": "Search AFIP activity...",
                }
            ),
            "jurisdiction": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CABA, BsAs, Córdoba…"
                }
            ),
            "is_primary": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    # -----------------------------
    # VALIDACIÓN UX PROFESIONAL
    # -----------------------------
    def clean(self):
        cleaned = super().clean()
        is_primary = cleaned.get("is_primary")
        company = self.instance.company

        if company is None:
            return cleaned

        # La primera actividad de la empresa debe quedar como primaria.
        existing_primary = (
            CompanyActivity.objects.filter(
                company=company,
                is_primary=True,
            )
            .exclude(id=self.instance.pk)
            .exists()
        )

        if is_primary:
            return cleaned

        if self.instance.pk is None and not existing_primary:
            cleaned["is_primary"] = True
            return cleaned

        if not existing_primary:
            raise forms.ValidationError(
                "At least one activity must be marked as primary."
            )

        return cleaned
