from django import forms
from django.forms import inlineformset_factory

from purchases.models.purchase import (
    Purchase,
    PurchaseLine,
    PurchasePerception,
    PurchaseRetention,
    PurchaseTax,
)


class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, company_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        if company_id is not None:
            self.fields["supplier"].queryset = self.fields["supplier"].queryset.filter(
                company_id=company_id,
                is_active=True,
            )

    class Meta:
        model = Purchase
        fields = ["supplier", "date", "invoice_number"]
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "invoice_number": forms.TextInput(attrs={"class": "form-control"}),
        }


class PurchaseLineForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data["unit_price"]
        if unit_price < 0:
            raise forms.ValidationError("Unit price cannot be negative.")
        return unit_price

    class Meta:
        model = PurchaseLine
        fields = ["description", "quantity", "unit_price", "expense_account"]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "expense_account": forms.Select(attrs={"class": "form-control"}),
        }


PurchaseLineFormSet = inlineformset_factory(
    Purchase,
    PurchaseLine,
    form=PurchaseLineForm,
    extra=1,
    can_delete=True,
)


class PurchaseTaxForm(forms.ModelForm):
    class Meta:
        model = PurchaseTax
        fields = ["vat_type", "base_amount", "amount"]
        widgets = {
            "vat_type": forms.Select(attrs={"class": "form-control"}),
            "base_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.get("instance")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        vat_type = cleaned.get("vat_type")

        if not self.purchase:
            return cleaned

        supplier = self.purchase.supplier
        profile = supplier.tax_profile

        if not profile:
            raise forms.ValidationError("Supplier has no tax profile assigned.")

        if vat_type in ["21", "105", "27"] and profile.vat_exempt:
            raise forms.ValidationError(
                "Supplier cannot apply VAT because the profile is marked as VAT exempt."
            )

        if vat_type == "0" and not profile.vat_exempt:
            raise forms.ValidationError(
                "Supplier is not VAT exempt; cannot use VAT 0%."
            )

        return cleaned


PurchaseTaxFormSet = inlineformset_factory(
    Purchase,
    PurchaseTax,
    form=PurchaseTaxForm,
    extra=1,
    can_delete=True,
)


class PurchasePerceptionForm(forms.ModelForm):
    class Meta:
        model = PurchasePerception
        fields = ["perception_type", "amount"]
        widgets = {
            "perception_type": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.get("instance")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        perception_type = cleaned.get("perception_type")

        if not self.purchase:
            return cleaned

        supplier = self.purchase.supplier
        profile = supplier.tax_profile

        if not profile:
            raise forms.ValidationError("Supplier has no tax profile assigned.")

        if perception_type == "IIBB" and profile.iibb_status == "NO_CORRESPONDE":
            raise forms.ValidationError("Supplier is not registered for IIBB.")

        if perception_type == "IVA" and profile.vat_exempt:
            raise forms.ValidationError("Supplier cannot apply IVA perceptions.")

        return cleaned


PurchasePerceptionFormSet = inlineformset_factory(
    Purchase,
    PurchasePerception,
    form=PurchasePerceptionForm,
    extra=1,
    can_delete=True,
)


class PurchaseRetentionForm(forms.ModelForm):
    class Meta:
        model = PurchaseRetention
        fields = ["retention_type", "amount"]
        widgets = {
            "retention_type": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.get("instance")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        retention_type = cleaned.get("retention_type")

        if not self.purchase:
            return cleaned

        supplier = self.purchase.supplier
        profile = supplier.tax_profile

        if not profile:
            raise forms.ValidationError("Supplier has no tax profile assigned.")

        if retention_type == "GAN" and profile.ganancias_status == "NO_CORRESPONDE":
            raise forms.ValidationError(
                "Supplier is not subject to Ganancias retention."
            )

        if retention_type == "IVA" and profile.vat_exempt:
            raise forms.ValidationError("Supplier is not subject to IVA retention.")

        if retention_type == "SUSS" and not profile.uses_retentions:
            raise forms.ValidationError("Supplier is not subject to SUSS retention.")

        return cleaned


PurchaseRetentionFormSet = inlineformset_factory(
    Purchase,
    PurchaseRetention,
    form=PurchaseRetentionForm,
    extra=1,
    can_delete=True,
)
