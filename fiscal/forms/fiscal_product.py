from django import forms
from fiscal.models import FiscalProduct
from fiscal.models.tax import Tax

class FiscalProductForm(forms.ModelForm):
    class Meta:
        model = FiscalProduct
        fields = [
            "name",
            "price",
            "tax",
            "vat_rate",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "tax": forms.Select(attrs={"class": "form-control"}),
            "vat_rate": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tax"].queryset = Tax.objects.filter(enabled=True)
