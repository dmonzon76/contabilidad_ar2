from django import forms
from sales.models.sale_item import SaleItem


class SaleItemForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data["unit_price"]
        if unit_price < 0:
            raise forms.ValidationError("Unit price cannot be negative.")
        return unit_price

    class Meta:
        model = SaleItem
        fields = [
            "description",
            "quantity",
            "unit_price",
        ]
