from decimal import Decimal

from django.db import models

from company.models import Company


class ThirdPartyTaxProfile(models.Model):
    """
    Perfil Fiscal de Terceros (Proveedores / Clientes).
    Define la condición impositiva AFIP/Provincial y parametriza:
    1. Percepciones que el tercero nos aplica (si es Agente de Percepción).
    2. Retenciones que nuestra empresa debe practicarle al realizar pagos.
    """

    AFIP_CATEGORY_CHOICES = [
        ("RI", "Responsable Inscripto"),
        ("MONO", "Monotributo"),
        ("EX", "Exento"),
        ("CF", "Consumidor Final"),
        ("NR", "No Responsable"),
        ("MT", "Monotributo Social"),
    ]

    GANANCIAS_STATUS_CHOICES = [
        ("INSCRIPTO", "Inscripto (Sujeto a Retención RG 830)"),
        ("EXENTO", "Exento (Certificado de Exención)"),
        ("NO_CORRESPONDE", "No Corresponde (Monotributista / Individuo)"),
    ]

    IIBB_STATUS_CHOICES = [
        ("LOCAL", "Inscripto Local"),
        ("MULTILATERAL", "Convenio Multilateral"),
        ("EXENTO", "Exento"),
        ("NO_INSCRIPTO", "No Inscripto"),
    ]

    JURISDICTION_CHOICES = [
        ("ARBA", "Buenos Aires (ARBA)"),
        ("AGIP", "CABA (AGIP)"),
        ("CORDOBA", "Córdoba"),
        ("SANTA_FE", "Santa Fe"),
        ("MENDOZA", "Mendoza"),
        ("TUCUMAN", "Tucumán"),
        ("OTRA", "Otra Jurisdicción"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="fiscal_tax_profiles",
    )

    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    tax_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    # ------------------------------------------------------------------
    # 1. CATEGORÍA PRINCIPAL Y AFIP
    # ------------------------------------------------------------------
    afip_category = models.CharField(max_length=10, choices=AFIP_CATEGORY_CHOICES, default="RI")

    # Condición IVA
    vat_21 = models.BooleanField(default=True)
    vat_105 = models.BooleanField(default=False)
    vat_27 = models.BooleanField(default=False)
    vat_exempt = models.BooleanField(default=False)
    vat_non_taxed = models.BooleanField(default=False)

    # ------------------------------------------------------------------
    # 2. PERCEPCIONES SUFRIDAS (Lo que el proveedor nos percibe a nosotros)
    # ------------------------------------------------------------------
    is_iibb_perception_agent = models.BooleanField(
        default=False,
        help_text="Marcar si el proveedor es Agente de Percepción de IIBB (ARBA/AGIP).",
    )
    iibb_perception_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.0000"),
        help_text="Alícuota de percepción IIBB que el proveedor nos recarga en facturas (ej. 3.5%).",
    )
    perception_jurisdiction = models.CharField(
        max_length=50,
        choices=JURISDICTION_CHOICES,
        default="ARBA",
        blank=True,
        null=True,
    )

    is_iva_perception_agent = models.BooleanField(
        default=False,
        help_text="Marcar si el proveedor nos aplica percepciones de IVA.",
    )
    iva_perception_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.0000"),
        help_text="Alícuota de percepción IVA (ej. 3.0%).",
    )

    # ------------------------------------------------------------------
    # 3. RETENCIONES PRACTICADAS (Lo que le retenemos al tercero al pagarle)
    # ------------------------------------------------------------------
    ganancias_status = models.CharField(
        max_length=20,
        choices=GANANCIAS_STATUS_CHOICES,
        default="INSCRIPTO",
    )
    ganancias_regime = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Código/Concepto de régimen RG 830 (ej. Honorarios, Alquileres, Bienes).",
    )
    ganancias_retention_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.0000"),
        help_text="Alícuota fija o especial de retención de Ganancias.",
    )

    iibb_status = models.CharField(
        max_length=20,
        choices=IIBB_STATUS_CHOICES,
        default="LOCAL",
    )
    iibb_retention_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.0000"),
        help_text="Alícuota de retención de IIBB a aplicarle según padrón.",
    )

    iva_retention_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.0000"),
        help_text="Alícuota de retención de IVA (ej. 50% o 80% de la alícuota de IVA).",
    )

    suss_retention_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.0000"),
        help_text="Alícuota de retención de SUSS.",
    )

    # ------------------------------------------------------------------
    # 4. EXENCIONES Y BANDERAS GENERALES
    # ------------------------------------------------------------------
    is_iibb_exempt = models.BooleanField(default=False)
    is_ganancias_exempt = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Perfil Fiscal de Tercero"
        verbose_name_plural = "Perfiles Fiscales de Terceros"

    def __str__(self):
        return f"{self.name} ({self.tax_id})" if self.tax_id else self.name
