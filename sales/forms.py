from django import forms
from sales.models.sale import Sale
from sales.models.sale_item import SaleItem


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["customer", "date", "number", "net_amount", "iva_amount", "total_amount"]


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ["description", "quantity", "unit_price", "subtotal"]
