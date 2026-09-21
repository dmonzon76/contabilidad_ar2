from decimal import Decimal

from django.db import models
from django.utils import timezone

from company.models import Company
from customers.models import Customer


class Sale(models.Model):

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("ISSUED", "Issued"),
        ("CANCELLED", "Cancelled"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="sales",
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    # Permite reconstruir operaciones históricas
    date = models.DateField(
        default=timezone.now,
    )

    number = models.CharField(
        max_length=20,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    net_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    iva_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        related_name="sales_created",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"Sale {self.number} - {self.customer.name}"

    def recalc_totals(self):

        net = Decimal("0.00")
        iva = Decimal("0.00")
        cost = Decimal("0.00")

        for item in self.items.all():

            net += item.subtotal

            if item.tax and item.tax.is_vat:
                iva += item.subtotal * (item.tax.rate / Decimal("100"))

            cost += item.cost_subtotal

        self.net_amount = net
        self.iva_amount = iva
        self.total_amount = net + iva
        self.total_cost = cost

        super(Sale, self).save(
            update_fields=[
                "net_amount",
                "iva_amount",
                "total_amount",
                "total_cost",
            ]
        )

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        if is_new and not self.number:

            last = Sale.objects.filter(company=self.company).order_by("-id").first()

            if last and last.number and last.number.isdigit():
                next_number = int(last.number) + 1
            else:
                next_number = 1

            self.number = str(next_number).zfill(6)

        super().save(*args, **kwargs)
