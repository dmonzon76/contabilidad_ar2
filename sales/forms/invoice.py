from django import forms
from sales.models.invoice import Invoice
from sales.models.invoice_series import InvoiceSeries
from sales.models.customer import Customer


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["customer", "series", "is_service"]

    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company")
        super().__init__(*args, **kwargs)

        # Filtrar clientes por empresa activa
        self.fields["customer"].queryset = Customer.objects.filter(company=company)

        # Filtrar talonarios por empresa activa
        self.fields["series"].queryset = InvoiceSeries.objects.filter(company=company)
