from django.db import models
from company.models import Company

IVA_CONDITIONS = [
    ("RI", "Responsable Inscripto"),
    ("MONO", "Monotributo"),
    ("EX", "Exento"),
    ("CF", "Consumidor Final"),
    ("NR", "No Responsable"),
]


class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)
    tax_id = models.CharField(max_length=20, blank=True, null=True)
    iva_condition = models.CharField(
        max_length=10,
        choices=IVA_CONDITIONS,
        default="CF",
    )
    iibb_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_iibb_exempt = models.BooleanField(default=False)
    ganancias_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_ganancias_exempt = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def customer_list(request):
    company = request.active_company
    customers = Customer.objects.filter(company=company, is_active=True)
    return render(request, "customers/customer_list.html", {"customers": customers})
