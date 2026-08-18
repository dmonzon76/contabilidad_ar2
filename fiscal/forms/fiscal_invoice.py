from django import forms
from fiscal.models.fiscal_invoice import FiscalInvoice


class FiscalInvoiceForm(forms.ModelForm):
    class Meta:
        model = FiscalInvoice
        fields = [
            "voucher_type",
            "point_of_sale",
            "voucher_number",
            "subtotal",
            "vat_amount",
            "exempt_amount",
            "non_taxed_amount",
            "total",
            "cae",
            "cae_expiration",
        ]

        widgets = {
            "voucher_type": forms.Select(attrs={"class": "form-select"}),
            "point_of_sale": forms.NumberInput(attrs={"class": "form-control"}),
            "voucher_number": forms.NumberInput(attrs={"class": "form-control"}),
            "subtotal": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
            "vat_amount": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
            "exempt_amount": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
            "non_taxed_amount": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
            "total": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
            "cae": forms.TextInput(attrs={"class": "form-control", "readonly": True}),
            "cae_expiration": forms.DateInput(attrs={"class": "form-control", "readonly": True}),
        }
