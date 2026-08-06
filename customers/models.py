from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    # ✔ Cliente activo/inactivo (normativa argentina)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
