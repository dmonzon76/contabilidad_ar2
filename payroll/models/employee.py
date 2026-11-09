from django.db import models

from company.models import Company


class Employee(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    employee_number = models.CharField(
        max_length=20,
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    cuil = models.CharField(
        max_length=11,
        unique=True,
    )
    dni = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    nationality = models.CharField(
        max_length=100,
        default="Argentina",
    )

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    MARITAL_STATUS_CHOICES = [
        ("SINGLE", "Single"),
        ("MARRIED", "Married"),
        ("DIVORCED", "Divorced"),
        ("WIDOWED", "Widowed"),
        ("CIVIL_UNION", "Civil Union"),
    ]

    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
        null=True,
    )

    street = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    street_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    province = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    mobile_phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    emergency_contact_phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    bank_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    cbu = models.CharField(
        max_length=22,
        blank=True,
        null=True,
    )
    hire_date = models.DateField()

    termination_date = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "last_name",
            "first_name",
        ]

    def __str__(self):

        return (
            f"{self.last_name}, "
            f"{self.first_name}"
        )