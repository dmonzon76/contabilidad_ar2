from django import forms
from suppliers.models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name",
            "email",
            "phone",
            "address",
            "tax_id",
            "iva_condition",
            "iibb_rate",
            "is_iibb_exempt",
            "ganancias_rate",
            "is_ganancias_exempt",
            "is_active",
        ]
# suppliers/forms/supplier.py
from django import forms
from suppliers.models import Supplier, ThirdPartyTaxProfile
from suppliers.utils import validate_cuit  # función que agregamos

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name","email","phone","address",
            "tax_id","iva_condition","iibb_rate","is_iibb_exempt",
            "ganancias_rate","is_ganancias_exempt","tax_profile","is_active",
        ]
        widgets = {
            "tax_profile": forms.Select(attrs={"class":"form-select"}),
            "iva_condition": forms.Select(attrs={"class":"form-select"}),
        }

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get("tax_id")
        if tax_id:
            tax_id = tax_id.replace("-", "").strip()
            if not validate_cuit(tax_id):
                raise forms.ValidationError("CUIT inválido")
        return tax_id
