from django.db import models
from company.models import Company
from sales.models.customer import Customer
from sales.models.invoice_series import InvoiceSeries


class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    series = models.ForeignKey(InvoiceSeries, on_delete=models.PROTECT)

    number = models.IntegerField()  # asignado automáticamente
    date = models.DateField(auto_now_add=True)

    is_service = models.BooleanField(default=False)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    cae = models.CharField(max_length=20, blank=True, null=True)  # futuro AFIP

    def __str__(self):
        return f"{self.series.code}-{self.series.point_of_sale}-{self.number}"
