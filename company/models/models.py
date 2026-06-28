from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    AFIP_CATEGORY_CHOICES = [
        ("RI", "Responsable Inscripto"),
        ("MONO", "Monotributo"),
        ("EX", "Exento"),
        ("PYME", "PyME"),
        ("GC", "Gran Contribuyente"),
        ("PH", "Persona Humana"),
    ]

    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200, blank=True)
    tax_id = models.CharField(max_length=20, unique=True)  # CUIT

    afip_category = models.CharField(
        max_length=10,
        choices=AFIP_CATEGORY_CHOICES,
    )

    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Argentina")
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    start_date = models.DateField(null=True, blank=True)
    accounting_start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when accounting starts in this system"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.tax_id})"

    # ============================================================
    # PURCHASES SUMMARY (Dashboard)
    # ============================================================

    @property
    def purchases_totals(self):
        from purchases.models.purchase import Purchase
        purchases = Purchase.objects.filter(company=self)

        return {
            "net": sum(p.net_amount for p in purchases),
            "iva": sum(p.tax_amount for p in purchases),
            "total": sum(p.total_amount for p in purchases),
        }

    @property
    def last_purchase(self):
        from purchases.models.purchase import Purchase
        return Purchase.objects.filter(company=self).order_by("-date", "-id").first()

    # ============================================================
    # SALES SUMMARY (Dashboard)
    # ============================================================

    @property
    def sales_totals(self):
        try:
            from sales.models.sale import Sale
            sales = Sale.objects.filter(company=self)
            return {
                "net": sum(s.net_amount for s in sales),
                "iva": sum(s.tax_amount for s in sales),
                "total": sum(s.total_amount for s in sales),
            }
        except:
            return {"net": 0, "iva": 0, "total": 0}

    @property
    def last_sale(self):
        try:
            from sales.models.sale import Sale
            return Sale.objects.filter(company=self).order_by("-date", "-id").first()
        except:
            return None


class CompanyProfile(models.Model):
    GANANCIAS_STATUS_CHOICES = [
        ("INSCRIPTO", "Inscripto"),
        ("EXENTO", "Exento"),
        ("NO_CORRESPONDE", "No corresponde (Monotributista)"),
    ]

    IIBB_STATUS_CHOICES = [
        ("INSCRIPTO", "Inscripto"),
        ("EXENTO", "Exento"),
        ("NO_CORRESPONDE", "No corresponde"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="tax_profile",
    )

    vat_21 = models.BooleanField(default=True)
    vat_105 = models.BooleanField(default=False)
    vat_27 = models.BooleanField(default=False)
    vat_exempt = models.BooleanField(default=False)
    vat_non_taxed = models.BooleanField(default=False)

    iibb_status = models.CharField(
        max_length=20,
        choices=IIBB_STATUS_CHOICES,
        default="NO_CORRESPONDE",
    )

    ganancias_status = models.CharField(
        max_length=20,
        choices=GANANCIAS_STATUS_CHOICES,
        default="NO_CORRESPONDE",
    )

    uses_perceptions = models.BooleanField(default=False)
    uses_retentions = models.BooleanField(default=False)

    def __str__(self):
        return f"Tax profile for {self.company.name}"


class CompanyUser(models.Model):
    ROLE_CHOICES = [
        ("OWNER", "Owner"),
        ("ACCOUNTANT", "Accountant"),
        ("DATAENTRY", "Data Entry"),
        ("AUDITOR", "Auditor"),
        ("VIEWER", "Viewer"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_users",
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    can_view_accounting = models.BooleanField(default=True)
    can_edit_accounting = models.BooleanField(default=False)
    can_view_fiscal = models.BooleanField(default=True)
    can_edit_fiscal = models.BooleanField(default=False)
    can_view_documents = models.BooleanField(default=True)
    can_edit_documents = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "company")

    def __str__(self):
        return f"{self.user.username} @ {self.company.name} ({self.role})"
