# fiscal/forms/fiscal_invoice.py

from django import forms
from fiscal.models.fiscal_invoice import FiscalInvoice


class FiscalInvoiceForm(forms.ModelForm):
    class Meta:
        model = FiscalInvoice
        fields = []  # La factura no se edita manualmente
