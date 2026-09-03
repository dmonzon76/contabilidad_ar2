from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError

from company.models import Company
from fiscal.models.tax import Tax
from fiscal.models.electronic_voucher_book import ElectronicVoucherBook


class FiscalInvoice(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="fiscal_invoices",
    )

    voucher_book = models.ForeignKey(
        ElectronicVoucherBook,
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    number = models.IntegerField()
    cae = models.CharField(max_length=20, blank=True, null=True)
    cae_expiration = models.DateField(blank=True, null=True)

    date = models.DateField()
    customer_name = models.CharField(max_length=255)
    customer_tax_id = models.CharField(max_length=20, blank=True, null=True)

    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    vat_21 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_105 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_27 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_exempt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_non_taxed = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    perception_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retention_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    is_closed = models.BooleanField(default=False)
    cae_due_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def determine_voucher_type(self):
        company_cat = self.company.tax_profile.category
        customer_cat = self.customer.tax_profile.category

        # Empresa Responsable Inscripto
        if company_cat == "RI":

            # Cliente Responsable Inscripto → Factura A
            if customer_cat == "RI":
                return "A"

        # Cliente Monotributo → Factura B
        if customer_cat == "MONO":
            return "B"

        # Cliente Consumidor Final
        if customer_cat == "CF":
            # AFIP: si supera $100.000 → A
            if self.total_amount >= 100000:
                return "A"
            return "B"

        # Cliente Exento / No alcanzado → B
        if customer_cat in ["EX", "NA"]:
            return "B"

        # Cliente extranjero → B
        if customer_cat == "EXT":
            return "B"

        # Empresa Monotributo → siempre C
        if company_cat == "MONO":
            return "C"

        # Empresa Exenta → Factura E
        if company_cat == "EX":
            return "E"

        # Default
        return "B"

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        if self.voucher_book:
            return f"Factura {self.voucher_book.voucher_type} {self.number}"
        return f"Factura {self.number}"

    @staticmethod
    def next_number(company, point_of_sale, voucher_type):
        book = (
            ElectronicVoucherBook.objects.filter(
                company=company,
                point_of_sale=point_of_sale,
                voucher_type=voucher_type,
                enabled=True,
            )
            .order_by("-current_number")
            .first()
        )

        if not book:
            raise ValueError(
                "No active electronic voucher book found for this company and type."
            )

        return book.next_number()

    def calculate_totals(self):
        net = Decimal("0.00")
        tax_total = Decimal("0.00")

        vat_21 = Decimal("0.00")
        vat_105 = Decimal("0.00")
        vat_27 = Decimal("0.00")
        vat_exempt = Decimal("0.00")
        vat_non_taxed = Decimal("0.00")

        for line in self.lines.all():
            line_total = line.line_total
            net += line_total

            if line.tax is None:
                continue

            tax_obj = line.tax
            tax_amount = line.tax_amount
            tax_total += tax_amount

            if tax_obj.afip_code == 5:
                vat_21 += tax_amount
            elif tax_obj.afip_code == 4:
                vat_105 += tax_amount
            elif tax_obj.afip_code == 6:
                vat_27 += tax_amount
            elif tax_obj.afip_code == 1:
                vat_exempt += line_total
            elif tax_obj.afip_code == 2:
                vat_non_taxed += line_total

        self.net_amount = net
        self.tax_amount = tax_total
        self.total_amount = net + tax_total

        self.vat_21 = vat_21
        self.vat_105 = vat_105
        self.vat_27 = vat_27
        self.vat_exempt = vat_exempt
        self.vat_non_taxed = vat_non_taxed

        self.save(
            update_fields=[
                "net_amount",
                "tax_amount",
                "total_amount",
                "vat_21",
                "vat_105",
                "vat_27",
                "vat_exempt",
                "vat_non_taxed",
            ]
        )

    def finalize(self):
        if self.is_closed:
            raise ValueError("Invoice already finalized")

        if not self.lines.exists():
            raise ValueError("Cannot finalize invoice without lines")

        self.calculate_totals()

        if self.number is None or self.number <= 0:
            self.number = self.assign_number()

        self.is_closed = True
        self.save(update_fields=["is_closed", "cae_due_date", "number"])
        return True

    def clean(self):
        if self.number <= 0:
            raise ValidationError("Invoice number must be positive.")

        if self.voucher_book is None:
            raise ValidationError("Voucher book is required.")

        if self.voucher_book.company != self.company:
            raise ValidationError("Voucher book belongs to another company.")

        if not self.voucher_book.enabled:
            raise ValidationError("Voucher book is disabled.")

    def assign_number(self):
        if self.voucher_book is None:
            raise ValidationError("Voucher book is required.")
        self.number = self.voucher_book.next_number()
