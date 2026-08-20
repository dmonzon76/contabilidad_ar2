from django import forms
from sales.models.sale import Sale


class SaleForm(forms.ModelForm):
    def __init__(self, *args, company_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company_id is not None:
            self.fields["customer"].queryset = self.fields["customer"].queryset.filter(
                company_id=company_id,
                is_active=True,
            )

    class Meta:
        model = Sale
        fields = [
            "customer",
        ]
