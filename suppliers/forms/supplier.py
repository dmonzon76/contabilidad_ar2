from django import forms

from suppliers.models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier

        fields = [
            "name",
            "tax_profile",
            "email",
            "phone",
            "address",
            
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Razón Social del Proveedor",
                }
            ),
            "tax_profile": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }