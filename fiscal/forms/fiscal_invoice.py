from django import forms
from fiscal.models import FiscalInvoice


class FiscalInvoiceForm(forms.ModelForm):
    class Meta:
        model = FiscalInvoice
        fields = [
            'company',
            'customer',
            'voucher_book',
            'voucher_number',
            'subtotal',
            'vat_amount',
            'total',
            'cae',
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'voucher_book': forms.Select(attrs={'class': 'form-control'}),
            'voucher_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'vat_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'cae': forms.TextInput(attrs={'class': 'form-control'}),
        }
