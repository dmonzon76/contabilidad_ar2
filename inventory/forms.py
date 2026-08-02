from django import forms
from .models import InventoryItem, InventoryMovement

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["product", "quantity", "min_stock"]


class InventoryMovementForm(forms.ModelForm):
    class Meta:
        model = InventoryMovement
        fields = ["movement_type", "quantity", "note"]
