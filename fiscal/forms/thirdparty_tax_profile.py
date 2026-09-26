from django import forms

from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile


class ThirdPartyTaxProfileForm(forms.ModelForm):
    class Meta:
        model = ThirdPartyTaxProfile
        fields = [
            # Categoria AFIP
            "afip_category",
            # Condiciones IVA
            "vat_21",
            "vat_105",
            "vat_27",
            "vat_exempt",
            "vat_non_taxed",
            # Percepciones Sufridas (Proveedor Agente de Percepción)
            "is_iibb_perception_agent",
            "iibb_perception_rate",
            "perception_jurisdiction",
            "is_iva_perception_agent",
            "iva_perception_rate",
            # Retenciones Practicadas (A aplicar al pagarle)
            "ganancias_status",
            "ganancias_regime",
            "ganancias_retention_rate",
            "iibb_status",
            "iibb_retention_rate",
            "iva_retention_rate",
            "suss_retention_rate",
            # Exenciones Generales
            "is_iibb_exempt",
            "is_ganancias_exempt",
        ]
        widgets = {
            "afip_category": forms.Select(attrs={"class": "form-control"}),
            "perception_jurisdiction": forms.Select(attrs={"class": "form-control"}),
            "ganancias_status": forms.Select(attrs={"class": "form-control"}),
            "ganancias_regime": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ej. Régimen RG 830 / Honorarios"}
            ),
            "iibb_status": forms.Select(attrs={"class": "form-control"}),
            # Alícuotas numéricas
            "iibb_perception_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "iva_perception_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "ganancias_retention_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "iibb_retention_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "iva_retention_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "suss_retention_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            # Banderas / Checkboxes
            "vat_21": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_105": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_27": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_exempt": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "vat_non_taxed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_iibb_perception_agent": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_iva_perception_agent": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_iibb_exempt": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_ganancias_exempt": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
