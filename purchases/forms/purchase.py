from django import forms
from django.forms import inlineformset_factory

from purchases.models.purchase import (
    Purchase,
    PurchaseLine,
    PurchaseTax,
    PurchasePerception,
    PurchaseRetention,
)


# -----------------------------
# Purchase (header)
# -----------------------------
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


# -----------------------------
# Purchase Line
# -----------------------------
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
    Purchase, PurchaseLine, form=PurchaseLineForm, extra=1, can_delete=True
)


# -----------------------------
# Purchase Tax
# -----------------------------
class PurchaseTaxForm(forms.ModelForm):
    class Meta:
        model = PurchaseTax
        fields = ["vat_type", "base_amount", "amount"]
        widgets = {
            "vat_type": forms.Select(attrs={"class": "form-control"}),
            "base_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }


PurchaseTaxFormSet = inlineformset_factory(
    Purchase, PurchaseTax, form=PurchaseTaxForm, extra=1, can_delete=True
)


# -----------------------------
# Purchase Perception
# -----------------------------
class PurchasePerceptionForm(forms.ModelForm):
    class Meta:
        model = PurchasePerception
        fields = ["perception_type", "amount"]
        widgets = {
            "perception_type": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }


PurchasePerceptionFormSet = inlineformset_factory(
    Purchase, PurchasePerception, form=PurchasePerceptionForm, extra=1, can_delete=True
)


# -----------------------------
# Purchase Retention
# -----------------------------
class PurchaseRetentionForm(forms.ModelForm):
    class Meta:
        model = PurchaseRetention
        fields = ["retention_type", "amount"]
        widgets = {
            "retention_type": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }


PurchaseRetentionFormSet = inlineformset_factory(
    Purchase, PurchaseRetention, form=PurchaseRetentionForm, extra=1, can_delete=True
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
        self.purchase = kwargs.get("instance", None)
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

        # Ejemplos reales AFIP
        if vat_type in ["21", "105", "27"] and profile.vat_exempt:
            raise forms.ValidationError(
                "Supplier cannot apply VAT because the profile is marked as VAT exempt."
            )

        if vat_type == "0" and not profile.vat_exempt:
            raise forms.ValidationError(
                "Supplier is not VAT exempt; cannot use VAT 0%."
            )

        return cleaned


class PurchasePerceptionForm(forms.ModelForm):
    class Meta:
        model = PurchasePerception
        fields = ["perception_type", "amount"]
        widgets = {
            "perception_type": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        ptype = cleaned.get("perception_type")

        if not self.purchase:
            return cleaned

        supplier = self.purchase.supplier
        profile = supplier.tax_profile

        if not profile:
            raise forms.ValidationError("Supplier has no tax profile assigned.")

        if ptype == "IIBB" and profile.iibb_status == "NO_CORRESPONDE":
            raise forms.ValidationError("Supplier is not registered for IIBB.")

        if ptype == "IVA" and profile.vat_exempt:
            raise forms.ValidationError("Supplier cannot apply IVA perceptions.")

        return cleaned


class PurchaseRetentionForm(forms.ModelForm):
    class Meta:
        model = PurchaseRetention
        fields = ["retention_type", "amount"]
        widgets = {
            "retention_type": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        rtype = cleaned.get("retention_type")

        if not self.purchase:
            return cleaned

        supplier = self.purchase.supplier
        profile = supplier.tax_profile

        if not profile:
            raise forms.ValidationError("Supplier has no tax profile assigned.")

        if rtype == "GAN" and profile.ganancias_status == "NO_CORRESPONDE":
            raise forms.ValidationError(
                "Supplier is not subject to Ganancias retention."
            )

        if rtype == "IVA" and profile.vat_exempt:
            raise forms.ValidationError("Supplier is not subject to IVA retention.")

        if rtype == "SUSS" and not profile.uses_retentions:
            raise forms.ValidationError("Supplier is not subject to SUSS retention.")

        return cleaned
