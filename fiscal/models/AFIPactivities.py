from django.db import models

class AFIPActivity(models.Model):
    code = models.CharField(max_length=6, unique=True)
    description = models.CharField(max_length=255)
    description_long = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.description}"
