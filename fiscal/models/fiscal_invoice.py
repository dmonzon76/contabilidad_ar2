from django.db import models
from company.models import Company
from sales.models.customer import Customer
from fiscal.models.electronic_voucher_book import ElectronicVoucherBook


class FiscalInvoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    voucher_book = models.ForeignKey(ElectronicVoucherBook, on_delete=models.PROTECT)
    voucher_number = models.IntegerField()  # correlativo AFIP interno

    date = models.DateField(auto_now_add=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    cae = models.CharField(max_length=20, blank=True, null=True)  # futuro AFIP

    def __str__(self):
        return f"{self.voucher_book.voucher_type}-{self.voucher_book.point_of_sale}-{self.voucher_number}"
