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

        # Si el usuario marca primaria → OK
        if is_primary:
            return cleaned

        # Si NO marca primaria, pero es la única primaria → error UX
        if not CompanyActivity.objects.filter(
            company=company,
            is_primary=True
        ).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                "At least one activity must be marked as primary."
            )

        return cleaned
