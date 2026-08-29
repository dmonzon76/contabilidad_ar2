from django import forms
from fiscal.models import FiscalService
from fiscal.models.tax import Tax

class FiscalServiceForm(forms.ModelForm):
    class Meta:
        model = FiscalService
        fields = [
            "name",
            "description",
            "price",
            "tax",
            "vat_rate",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "tax": forms.Select(attrs={"class": "form-control"}),
            "vat_rate": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tax"].queryset = Tax.objects.filter(enabled=True)
