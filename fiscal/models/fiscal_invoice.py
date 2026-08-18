from decimal import Decimal
from django.db import models
from company.models import Company
from sales.models.sale import Sale
from sales.models.customer import Customer


class FiscalInvoice(models.Model):
    """
    Factura fiscal argentina vinculada a una venta comercial (Sale).
    Genera número fiscal, CAE, totales y soporta ítems exentos/no gravados.
    """

    # Empresa activa (no se pide en formularios)
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="fiscal_invoices"
    )

    # Cliente (se toma de la venta)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="fiscal_invoices"
    )

    # VENTA vinculada (clave del flujo)
    sale = models.OneToOneField(
        Sale,
        on_delete=models.PROTECT,
        related_name="fiscal_invoice"
    )

    # Tipo de comprobante (A, B, C, NC, ND)
    voucher_type = models.CharField(
        max_length=5,
        choices=[
            ("A", "Factura A"),
            ("B", "Factura B"),
            ("C", "Factura C"),
            ("NC", "Nota de Crédito"),
            ("ND", "Nota de Débito"),
        ],
        default="B"
    )

    # Punto de venta AFIP
    point_of_sale = models.IntegerField(default=1)

    # Número fiscal correlativo
    voucher_number = models.IntegerField()

    # Fecha de emisión
    date = models.DateField(auto_now_add=True)

    # Totales fiscales
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    exempt_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    non_taxed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # CAE (simulado por ahora)
    cae = models.CharField(max_length=20, blank=True, null=True)
    cae_expiration = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.voucher_type}-{self.point_of_sale}-{self.voucher_number}"

    # ---------------------------------------------------------
    # Cálculo fiscal basado en los ítems de la venta
    # ---------------------------------------------------------
    def calculate_totals(self):
        net = Decimal("0.00")
        vat = Decimal("0.00")
        exempt = Decimal("0.00")
        non_taxed = Decimal("0.00")

        for item in self.sale.items.all():
            if item.tax_category == "GRAVADO":
                net += item.subtotal
                vat += item.subtotal * Decimal("0.21")
            elif item.tax_category == "EXENTO":
                exempt += item.subtotal
            elif item.tax_category == "NO_GRAVADO":
                non_taxed += item.subtotal

        self.subtotal = net
        self.vat_amount = vat
        self.exempt_amount = exempt
        self.non_taxed_amount = non_taxed
        self.total = net + vat + exempt + non_taxed

    # ---------------------------------------------------------
    # Generación de número fiscal correlativo
    # ---------------------------------------------------------
    @staticmethod
    def next_number(company, point_of_sale, voucher_type):
        last = FiscalInvoice.objects.filter(
            company=company,
            point_of_sale=point_of_sale,
            voucher_type=voucher_type
        ).order_by("-voucher_number").first()

        return (last.voucher_number + 1) if last else 1

    # ---------------------------------------------------------
    # Generación de CAE (simulado)
    # ---------------------------------------------------------
    def generate_cae(self):
        import random
        from datetime import date, timedelta

        self.cae = str(random.randint(10000000, 99999999))
        self.cae_expiration = date.today() + timedelta(days=10)

    # ---------------------------------------------------------
    # Guardado completo
    # ---------------------------------------------------------
    def finalize(self):
        self.calculate_totals()
        self.generate_cae()
        self.save()
