from django import forms
from sales.models.customer import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "tax_id",
            "email",
            "phone",
            "address",
            "city",
            "province",
            "country",
            "customer_type",
            "notes",
            "is_active",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
