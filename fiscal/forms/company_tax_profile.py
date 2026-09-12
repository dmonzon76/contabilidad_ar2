from django import forms
from fiscal.models.company_profile import CompanyProfile

class CompanyTaxProfileForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()

        # La compañía viene del instance, no del form
        company = self.instance.company

        # Buscar otros perfiles de la misma compañía
        qs = CompanyProfile.objects.filter(company=company)

        # Excluir el actual si estamos editando
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            # Error asignado al campo NON-FIELD, porque company no está en el form
            raise forms.ValidationError(
                "This company already has a tax profile."
            )

        return cleaned_data
