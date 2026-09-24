from django import forms

from sales.models.sale import Sale
from customers.models import Customer


class SaleForm(forms.ModelForm):

    def __init__(self, *args, company_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["customer"].queryset = Customer.objects.none()

        if company_id is not None:
            self.fields["customer"].queryset = Customer.objects.filter(
                company_id=company_id,
                is_active=True,
            ).order_by("name")

        self.fields["date"].widget = forms.DateInput(
            attrs={
                "type": "date",
            }
        )
        self.fields["date"].required = False

    class Meta:
        model = Sale

        fields = [
            "customer",
            "date",
        ]
