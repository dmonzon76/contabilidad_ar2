from django.db import models
from django.utils import timezone
from company.models import Company


class FiscalYear(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OPEN")

    class Meta:
        unique_together = ("company", "year")
        ordering = ["-year"]

    def __str__(self):
        return f"{self.company.name} - Fiscal Year {self.year}"


class Period(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("LOCKED", "Locked"),
    ]

    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE, related_name="periods")
    month = models.IntegerField()  # 1 = January, 12 = December
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OPEN")

    class Meta:
        unique_together = ("fiscal_year", "month")
        ordering = ["fiscal_year__year", "month"]

    def __str__(self):
        return f"{self.fiscal_year.year} - {self.month:02d} ({self.status})"























