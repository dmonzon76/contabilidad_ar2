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
        instance = kwargs.get("instance")
        self.purchase = (
            instance.purchase
            if instance and hasattr(instance, "purchase") and instance.purchase
            else None
        )
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
            "tax": TaxSelect(attrs={"class": "form-control"}),
            "base_amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, company_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar solo impuestos de IVA, Exento o No Gravado que estén activos
        self.fields["tax"].queryset = self.fields["tax"].queryset.filter(
            Q(is_vat=True) | Q(is_exempt=True) | Q(is_non_taxed=True),
            enabled=True,
        )

        # Asignar tax_rates al widget ya instanciado por Django (sin re-instanciarlo)
        self.fields["tax"].widget.tax_rates = {
            str(tax.pk): str(tax.rate) for tax in self.fields["tax"].queryset
        }

    def clean(self):
        cleaned = super().clean()
        tax = cleaned.get("tax")
        purchase = getattr(self, "purchase", None) or getattr(
            self.instance, "purchase", None
        )
        if not purchase or not getattr(purchase, "supplier", None):
            return cleaned

        profile = getattr(purchase.supplier, "tax_profile", None)
        if not profile or tax is None:
            return cleaned

        iva_condition = getattr(profile, "iva_condition", "")
        if tax.is_vat and iva_condition == "EX":
            raise forms.ValidationError(
                "El proveedor está exento de IVA y no puede aplicar alícuotas de IVA."
            )
        if tax.is_exempt and iva_condition != "EX":
            raise forms.ValidationError(
                "El proveedor no está exento de IVA; no puede aplicar alícuota Exenta."
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

    def __init__(self, *args, company_id=None, parent_purchase=None, **kwargs):
        instance = kwargs.get("instance")
        self.purchase = parent_purchase or (
            instance.purchase
            if instance and hasattr(instance, "purchase") and instance.purchase
            else None
        )
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        perception_type = cleaned.get("perception_type")

        if not self.purchase or not getattr(self.purchase, "supplier", None):
            return cleaned

        supplier = self.purchase.supplier
        profile = getattr(supplier, "tax_profile", None)

        if not profile:
            return cleaned

        if perception_type == "IIBB" and getattr(profile, "is_iibb_exempt", False):
            raise forms.ValidationError("El proveedor está exento de IIBB.")

        if perception_type == "IVA" and getattr(profile, "iva_condition", "") == "EX":
            raise forms.ValidationError(
                "El proveedor exento de IVA no aplica percepciones de IVA."
            )

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

    def __init__(self, *args, company_id=None, parent_purchase=None, **kwargs):
        instance = kwargs.get("instance")
        self.purchase = parent_purchase or (
            instance.purchase
            if instance and hasattr(instance, "purchase") and instance.purchase
            else None
        )
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        retention_type = cleaned.get("retention_type")

        if not self.purchase or not getattr(self.purchase, "supplier", None):
            return cleaned

        supplier = self.purchase.supplier
        profile = getattr(supplier, "tax_profile", None)

        if not profile:
            return cleaned

        if retention_type == "GAN" and getattr(profile, "is_ganancias_exempt", False):
            raise forms.ValidationError(
                "Supplier is not subject to Ganancias retention."
            )

        if retention_type == "IVA" and getattr(profile, "iva_condition", "") == "EX":
            raise forms.ValidationError("Supplier is not subject to IVA retention.")

        return cleaned


PurchaseRetentionFormSet = inlineformset_factory(
    Purchase,
    PurchaseRetention,
    form=PurchaseRetentionForm,
    extra=1,
    can_delete=True,
)
