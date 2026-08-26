from django.db import models, transaction

class FiscalInvoice(models.Model):
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    customer = models.ForeignKey("customers.Customer", on_delete=models.PROTECT)
    sale = models.OneToOneField("sales.Sale", on_delete=models.PROTECT)

    voucher_type = models.CharField(max_length=5)
    point_of_sale = models.PositiveIntegerField()
    voucher_number = models.PositiveIntegerField()

    date = models.DateField(auto_now_add=True)

    # Totales
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    exempt_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    non_taxed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    is_closed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "point_of_sale", "voucher_type", "voucher_number"],
                name="unique_fiscal_invoice_number_per_company"
            )
        ]

    @staticmethod
    @transaction.atomic
    def next_number(company, point_of_sale, voucher_type):
        """
        Devuelve el próximo número fiscal de forma segura.
        Evita condiciones de carrera usando select_for_update().
        """

        qs = (
            FiscalInvoice.objects
            .select_for_update()
            .filter(
                company=company,
                point_of_sale=point_of_sale,
                voucher_type=voucher_type
            )
            .order_by("-voucher_number")
        )

        last = qs.first()
        return (last.voucher_number + 1) if last else 1
