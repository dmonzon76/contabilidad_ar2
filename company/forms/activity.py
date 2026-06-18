

from django import forms
from company.models import CompanyActivity


class CompanyActivityForm(forms.ModelForm):
    class Meta:
        model = CompanyActivity
        fields = ["code", "description", "is_primary", "jurisdiction"]

    def clean(self):
        cleaned = super().clean()
        is_primary = cleaned.get("is_primary")

        if is_primary and self.instance.company_id:
            CompanyActivity.objects.filter(
                company=self.instance.company
            ).update(is_primary=False)

        return cleaned


