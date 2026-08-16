from django import forms
from fiscal.models import FiscalInvoiceLine


class FiscalInvoiceLineForm(forms.ModelForm):
    class Meta:
        model = FiscalInvoiceLine
        fields = [
            'invoice',
            'description',
            'quantity',
            'price',
            'vat_rate',
        ]
        widgets = {
            'invoice': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'vat_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
