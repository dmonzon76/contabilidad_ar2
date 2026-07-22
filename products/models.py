from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"
