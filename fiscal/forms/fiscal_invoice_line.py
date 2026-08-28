# fiscal/forms/fiscal_invoice_line.py

from django import forms
from fiscal.models.fiscal_invoice_line import FiscalInvoiceLine
from fiscal.models.tax import Tax


class FiscalInvoiceLineForm(forms.ModelForm):
    class Meta:
        model = FiscalInvoiceLine
        fields = [
            "description",
            "quantity",
            "unit_price",
            "tax",
        ]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "tax": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)

        # Filtrar impuestos habilitados
        self.fields["tax"].queryset = Tax.objects.filter(enabled=True)
