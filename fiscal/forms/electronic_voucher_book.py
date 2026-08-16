from django import forms
from fiscal.models import ElectronicVoucherBook

class ElectronicVoucherBookForm(forms.ModelForm):
    class Meta:
        model = ElectronicVoucherBook
        fields = [
            'voucher_type',
            'point_of_sale',
            'current_number',
            'enabled',
        ]
