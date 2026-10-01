from django import forms

from customers.models import Customer
from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile
from sales.models.sale import Sale


class SaleForm(forms.ModelForm):

    def __init__(self, *args, company_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["customer"].queryset = Customer.objects.none()

        if company_id is not None:
            self.fields["customer"].queryset = Customer.objects.filter(
                company_id=company_id,
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

class SupplierForm(forms.ModelForm):

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        if company:
            self.fields["tax_profile"].queryset = (
                ThirdPartyTaxProfile.objects.filter(
                    company=company
                ).order_by("name")
            )