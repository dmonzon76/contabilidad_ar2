from django.db import models

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

    point_of_sale = models.IntegerField()  # PV autorizado por AFIP
    voucher_type = models.CharField(max_length=4, choices=VOUCHER_TYPES)

    current_number = models.IntegerField(default=1)  # correlativo electrónico
    enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_voucher_type_display()} - PV {self.point_of_sale}"

    def next_number(self):
        """
        Devuelve el próximo número correlativo y actualiza el talonario electrónico.
        """
        number = self.current_number
        self.current_number += 1
        self.save()
        return number
