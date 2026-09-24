from django import forms
from django.forms import inlineformset_factory

from purchases.models import (
    Purchase,
    PurchaseLine,
    PurchaseTax,
    PurchasePerception,
    PurchaseRetention,
)
from suppliers.models import Supplier
from fiscal.models import Tax
from accounting.models import Account


class PurchaseForm(forms.ModelForm):
    """
    Formulario para la cabecera del comprobante de compra.
    """

    class Meta:
        model = Purchase
        fields = ["supplier", "date", "invoice_number"]
        labels = {
            "supplier": "Proveedor",
            "date": "Fecha de Comprobante",
            "invoice_number": "Número de Factura / Comprobante",
        }
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "invoice_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0001-00000001",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company", None)
        company_id = kwargs.pop("company_id", None)
        super().__init__(*args, **kwargs)

        # Filtrar proveedores activos de la empresa actual
        if company:
            self.fields["supplier"].queryset = Supplier.objects.filter(
                company=company,
                is_active=True,
            )
        elif company_id is not None:
            self.fields["supplier"].queryset = Supplier.objects.filter(
                company_id=company_id,
                is_active=True,
            )


class PurchaseLineForm(forms.ModelForm):
    """
    Formulario para cada renglón o concepto individual de la compra.
    Permite asignar diferentes alícuotas de IVA y cuentas de gasto por línea.
    """

    class Meta:
        model = PurchaseLine
        fields = [
            "description",
            "quantity",
            "unit_price",
            "tax",
            "expense_account",
        ]
        labels = {
            "description": "Concepto / Descripción",
            "quantity": "Cantidad",
            "unit_price": "Precio Unitario (Neto)",
            "tax": "Alícuota IVA",
            "expense_account": "Cuenta de Gasto",
        }
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Consultoría / Producto / Capacitación",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.01",
                    "value": "1.00",
                }
            ),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.00",
                    "placeholder": "0.00",
                }
            ),
            "tax": forms.Select(attrs={"class": "form-select"}),
            "expense_account": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)

        if company:
            self.fields["tax"].queryset = Tax.objects.filter(
                company=company,
                is_active=True,
            )
            self.fields["expense_account"].queryset = Account.objects.filter(
                company=company,
                is_active=True,
            )


class PurchasePerceptionForm(forms.ModelForm):
    """
    Formulario para la carga de Percepciones Impositivas (IIBB, IVA, Municipal).
    """

    class Meta:
        model = PurchasePerception
        fields = ["perception_type", "amount"]
        labels = {
            "perception_type": "Tipo de Percepción",
            "amount": "Monto Percepción",
        }
        widgets = {
            "perception_type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.00",
                    "placeholder": "0.00",
                }
            ),
        }


class PurchaseRetentionForm(forms.ModelForm):
    """
    Formulario para la carga de Retenciones Impositivas (Ganancias, IVA, SUSS).
    """

    class Meta:
        model = PurchaseRetention
        fields = ["retention_type", "amount"]
        labels = {
            "retention_type": "Tipo de Retención",
            "amount": "Monto Retención",
        }
        widgets = {
            "retention_type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.00",
                    "placeholder": "0.00",
                }
            ),
        }


# --- FORMSETS INLINE ---

# Formset de líneas/conceptos de la compra
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
        fields = ["tax", "base_amount"]

    def __init__(self, *args, **kwargs):
        company_id = kwargs.pop("company_id", None)
        super().__init__(*args, **kwargs)

        if company_id is not None:
            self.fields["tax"].queryset = Tax.objects.filter(
                company_id=company_id,
                is_active=True,
            )


PurchaseTaxFormSet = inlineformset_factory(
    Purchase,
    PurchaseTax,
    form=PurchaseTaxForm,
    extra=0,
    can_delete=True,
)

# Formset de percepciones impositivas
PurchasePerceptionFormSet = inlineformset_factory(
    Purchase,
    PurchasePerception,
    form=PurchasePerceptionForm,
    extra=0,
    can_delete=True,
)

# Formset de retenciones impositivas
PurchaseRetentionFormSet = inlineformset_factory(
    Purchase,
    PurchaseRetention,
    form=PurchaseRetentionForm,
    extra=0,
    can_delete=True,
)
