from django.db import models
from company.models import Company


class InvoiceSeries(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)  # A, B, C, NC-A, ND-B, etc.
    point_of_sale = models.IntegerField()
    next_number = models.IntegerField(default=1)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ("company", "code", "point_of_sale")

    def __str__(self):
        return f"{self.company.name} – {self.code} {self.point_of_sale}"
