from django import forms
from fiscal.models import FiscalSale


class FiscalSaleForm(forms.ModelForm):
    class Meta:
        model = FiscalSale
        fields = [
            'sale',
            'voucher_book',
        ]
        widgets = {
            'sale': forms.Select(attrs={'class': 'form-control'}),
            'voucher_book': forms.Select(attrs={'class': 'form-control'}),
        }
