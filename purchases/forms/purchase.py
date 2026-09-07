from django import forms
from django.forms import inlineformset_factory
from django.db.models import Q

from purchases.models.purchase import (
    Purchase,
    PurchaseLine,
    PurchasePerception,
    PurchaseRetention,
    PurchaseTax,
)


class TaxSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        self.tax_rates = {}
        super().__init__(*args, **kwargs)

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        tax_id = str(value.value if hasattr(value, "value") else value)
        if tax_id in self.tax_rates:
            option["attrs"]["data-rate"] = self.tax_rates[tax_id]
        return option


# ============================================================
# PURCHASE HEADER FORM
# ============================================================


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


class PurchaseTaxForm(forms.ModelForm):
    class Meta:
        model = PurchaseTax
        fields = ["tax", "base_amount"]
        widgets = {
            "tax": forms.Select(attrs={"class": "form-control"}),
            "base_amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, company_id=None, **kwargs):
        self.purchase = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        self.fields["tax"].queryset = self.fields["tax"].queryset.filter(
            Q(is_vat=True) | Q(is_exempt=True) | Q(is_non_taxed=True),
            enabled=True,
        )
        tax_widget = TaxSelect(attrs={"class": "form-control"})
        tax_widget.tax_rates = {
            str(tax.pk): str(tax.rate) for tax in self.fields["tax"].queryset
        }
        self.fields["tax"].widget = tax_widget

    def clean(self):
        cleaned = super().clean()
        tax = cleaned.get("tax")

        if not self.purchase:
            return cleaned

        supplier = self.purchase.supplier
        profile = supplier.tax_profile

        if not profile:
            raise forms.ValidationError("Supplier has no tax profile assigned.")

        if tax is not None and tax.is_vat and profile.iva_condition == "EX":
            raise forms.ValidationError(
                "Supplier cannot apply VAT because the profile is marked as VAT exempt."
            )

        if tax is not None and tax.is_exempt and profile.iva_condition != "EX":
            raise forms.ValidationError(
                "Supplier is not VAT exempt; cannot use a 0% tax."
            )

        return cleaned


# ============================================================
# PURCHASE LINES
# ============================================================


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


# ============================================================
# PURCHASE TAXES (IVA)
# ============================================================


PurchaseTaxFormSet = inlineformset_factory(
    Purchase,
    PurchaseTax,
    form=PurchaseTaxForm,
    extra=1,
    can_delete=True,
)


# ============================================================
# PURCHASE PERCEPTIONS
# ============================================================


class PurchasePerceptionForm(forms.ModelForm):
    class Meta:
        model = PurchasePerception
        fields = ["perception_type"]
        widgets = {
            "perception_type": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, company_id=None, **kwargs):
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

        if perception_type == "IIBB" and profile.is_iibb_exempt:
            raise forms.ValidationError("Supplier is not registered for IIBB.")

        if perception_type == "IVA" and profile.iva_condition == "EX":
            raise forms.ValidationError("Supplier cannot apply IVA perceptions.")

        return cleaned


PurchasePerceptionFormSet = inlineformset_factory(
    Purchase,
    PurchasePerception,
    form=PurchasePerceptionForm,
    extra=1,
    can_delete=True,
)


# ============================================================
# PURCHASE RETENTIONS
# ============================================================


class PurchaseRetentionForm(forms.ModelForm):
    class Meta:
        model = PurchaseRetention
        fields = ["retention_type"]
        widgets = {
            "retention_type": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, company_id=None, **kwargs):
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

        if retention_type == "GAN" and profile.is_ganancias_exempt:
            raise forms.ValidationError(
                "Supplier is not subject to Ganancias retention."
            )

        if retention_type == "IVA" and profile.iva_condition == "EX":
            raise forms.ValidationError("Supplier is not subject to IVA retention.")

        return cleaned


PurchaseRetentionFormSet = inlineformset_factory(
    Purchase,
    PurchaseRetention,
    form=PurchaseRetentionForm,
    extra=1,
    can_delete=True,
)
