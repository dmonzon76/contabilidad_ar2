from django import forms

from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile
from suppliers.models import Supplier


class SupplierForm(forms.ModelForm):
    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            tax_profile_field = self.fields["tax_profile"]
            if not isinstance(tax_profile_field, forms.ModelChoiceField):
                raise TypeError("SupplierForm.tax_profile must be a model choice field")
            tax_profile_field.queryset = ThirdPartyTaxProfile.objects.filter(
                company=company
            ).order_by("name")

    class Meta:
        model = Supplier

        fields = [
            "name",
            "tax_id",
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
            "tax_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CUIT",
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
        }