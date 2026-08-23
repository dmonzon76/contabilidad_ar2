from django.db import models
from company.models import Company
from customers.models import Customer
from suppliers.models import Supplier
from sales.models.sale import Sale
from purchases.models.purchase import Purchase


class AccountMovement(models.Model):
    MOVEMENT_TYPES = [
        ("DEBIT", "Débito"),
        ("CREDIT", "Crédito"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Cliente o proveedor (uno de los dos)
    customer = models.ForeignKey(
        Customer, null=True, blank=True, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, null=True, blank=True, on_delete=models.CASCADE
    )

    # Origen del movimiento
    sale = models.ForeignKey(
        Sale, null=True, blank=True, on_delete=models.SET_NULL
    )
    purchase = models.ForeignKey(
        Purchase, null=True, blank=True, on_delete=models.SET_NULL
    )

    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        if self.customer:
            return f"CC Cliente {self.customer} - {self.amount}"
        if self.supplier:
            return f"CC Proveedor {self.supplier} - {self.amount}"
        return f"Movimiento CC {self.amount}"
