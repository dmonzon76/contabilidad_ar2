from django import forms
from fiscal.models import FiscalService


class FiscalServiceForm(forms.ModelForm):
    class Meta:
        model = FiscalService
        fields = [
            'name',
            'description',
            'price',
            'vat_rate',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'vat_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
