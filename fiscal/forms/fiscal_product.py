from django import forms
from fiscal.models import FiscalProduct


class FiscalProductForm(forms.ModelForm):
    class Meta:
        model = FiscalProduct
        fields = [
            'name',
            'price',
            'vat_rate',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'vat_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
