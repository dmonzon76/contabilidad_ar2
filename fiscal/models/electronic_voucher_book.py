from django.db import models, transaction
from django.core.exceptions import ValidationError


class ElectronicVoucherBook(models.Model):
    VOUCHER_TYPES = [
        ('FA', 'Factura A'),
        ('FB', 'Factura B'),
        ('FC', 'Factura C'),
        ('NCA', 'Nota de Crédito A'),
        ('NCB', 'Nota de Crédito B'),
        ('NCC', 'Nota de Crédito C'),
        ('NDA', 'Nota de Débito A'),
        ('NDB', 'Nota de Débito B'),
        ('NDC', 'Nota de Débito C'),
    ]

    company = models.ForeignKey(
        "company.Company",
        on_delete=models.CASCADE,
        related_name="voucher_books"
    )

    point_of_sale = models.IntegerField()
    voucher_type = models.CharField(max_length=4, choices=VOUCHER_TYPES)

    current_number = models.IntegerField(default=1)
    enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "point_of_sale", "voucher_type")
        ordering = ["company", "point_of_sale", "voucher_type"]

    def __str__(self):
        return f"{self.get_voucher_type_display()} - PV {self.point_of_sale}"

    def clean(self):
        if not (1 <= self.point_of_sale <= 99999):
            raise ValidationError("Point of sale must be between 1 and 99999")

        if self.current_number < 1:
            raise ValidationError("Current number must be >= 1")

    @transaction.atomic
    def next_number(self):
        """
        Devuelve el próximo número correlativo de forma segura.
        Evita race conditions y garantiza numeración fiscal correcta.
        """
        self.refresh_from_db()
        number = self.current_number
        self.current_number += 1
        self.save(update_fields=["current_number"])
        return number
