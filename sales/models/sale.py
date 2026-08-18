from decimal import Decimal
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

    # Número interno de venta (NO fiscal)
    # Se genera automáticamente, no lo ingresa el usuario.
    number = models.CharField(max_length=20, blank=True)

    # Totales comerciales
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Totales de costo (para CMV)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Generar número interno si está vacío
        if not self.number:
            last = Sale.objects.filter(company=self.company).order_by("-id").first()
            next_number = (int(last.number) + 1) if last and last.number.isdigit() else 1
            self.number = str(next_number).zfill(6)
        super().save(*args, **kwargs)

    def recalc_totals(self):
        """
        Recalcula:
        - neto
        - IVA
        - total
        - costo total (para CMV)
        - soporta ítems gravados, exentos y no gravados
        """
        from sales.models.sale_item import SaleItem

        net = Decimal("0.00")
        iva = Decimal("0.00")
        cost = Decimal("0.00")

        for item in self.items.all():

            # Suma del subtotal comercial
            net += item.subtotal

            # IVA solo si el ítem es gravado
            if item.tax_category == "GRAVADO":
                iva += item.subtotal * Decimal("0.21")

            # Suma del costo para CMV
            cost += item.cost_subtotal

        self.net_amount = net
        self.iva_amount = iva
        self.total_amount = net + iva
        self.total_cost = cost

        self.save()

    def __str__(self):
        return f"Sale {self.number} — {self.customer.name}"
