from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "company",
            "name",
            "sku",
            "description",
            "detail",
            "type",
            "income_account",
            "purchase_account",
            "tax",
            "price",
        ]

        widgets = {
            "type": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].required = True
        self.fields["type"].empty_label = None

        self.fields["type"].help_text = (
            "PRODUCT: Physical product with stock and inventory movements. SERVICE: Service without stock or inventory."
        )

        self.fields["name"].widget.attrs.update({"placeholder": "Product or Service Name"})

        self.fields["sku"].widget.attrs.update({"placeholder": "Unique Code"})

    def clean(self):
        cleaned_data = super().clean()

        product_type = cleaned_data.get("type")
        purchase_account = cleaned_data.get("purchase_account")

        if product_type == "SERVICE" and purchase_account:
            self.add_error("purchase_account", "Services normally should not use purchase accounts.")

        return cleaned_data
