from django import forms
from sales.models.sale import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            "customer",
            "date",
            "number",
            "net_amount",
            "iva_amount",
            "total_amount",
        ]
