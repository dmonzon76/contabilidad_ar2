from django import forms
from sales.models.invoice_line import InvoiceLine



class InvoiceLineForm(forms.ModelForm):
    class Meta:
        model = InvoiceLine
        fields = ["product", "description", "quantity", "unit_price", "vat_rate"]

    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company")
        super().__init__(*args, **kwargs)

        # Filtrar productos por empresa
        self.fields["product"].queryset = Product.objects.filter(company=company)

from django.forms import inlineformset_factory
from sales.models.invoice import Invoice

InvoiceLineFormSet = inlineformset_factory(
    Invoice,
    InvoiceLine,
    form=InvoiceLineForm,
    extra=1,
    can_delete=True
)
