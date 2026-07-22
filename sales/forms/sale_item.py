from django import forms
from sales.models.sale_item import SaleItem

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = [
            "description",
            "quantity",
            "unit_price",
        ]
