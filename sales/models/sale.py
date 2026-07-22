from django.db import models
from company.models import Company
from sales.models.customer import Customer

class Sale(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="sales"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales"
    )

    date = models.DateField(auto_now_add=True)
    number = models.CharField(max_length=20)

    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Sale {self.number} — {self.customer.name}"

