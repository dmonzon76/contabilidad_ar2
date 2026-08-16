from django.db import models
from sales.models.sale import Sale
from fiscal.models.electronic_voucher_book import ElectronicVoucherBook
from fiscal.models.fiscal_invoice import FiscalInvoice


class FiscalSale(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    voucher_book = models.ForeignKey(ElectronicVoucherBook, on_delete=models.PROTECT)
    invoice = models.OneToOneField(FiscalInvoice, on_delete=models.SET_NULL, null=True, blank=True)

    def generate_invoice(self):
        """
        Genera una factura fiscal a partir de la venta comercial.
        """
        number = self.voucher_book.next_number()

        invoice = FiscalInvoice.objects.create(
            company=self.sale.company,
            customer=self.sale.customer,
            voucher_book=self.voucher_book,
            voucher_number=number,
            subtotal=self.sale.subtotal,
            vat_amount=self.sale.vat_amount,
            total=self.sale.total,
        )

        self.invoice = invoice
        self.save()

        return invoice

    def __str__(self):
        return f"FiscalSale #{self.id} → Invoice {self.invoice}"
