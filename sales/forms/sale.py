from django import forms
from sales.models.customer import Customer
from sales.models.sale import Sale


class SaleForm(forms.ModelForm):
    def __init__(self, *args, company_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].queryset = Customer.objects.none()
        if company_id is not None:
            self.fields["customer"].queryset = Customer.objects.filter(
                company_id=company_id,
                is_active=True,
            ).order_by("name")

    class Meta:
        model = Sale
        fields = [
            "customer",
        ]
