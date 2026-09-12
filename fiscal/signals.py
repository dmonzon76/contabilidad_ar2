from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounting.models import Account, FiscalYear, Period
from company.models import Company
from fiscal.models.company_profile import CompanyProfile

DEFAULT_ACCOUNT_CODES = [
    ("CAJA", "Caja", "ASSET"),
    ("CLIENTES", "Clientes", "ASSET"),
    ("VENTAS", "Ventas", "INCOME"),
    ("IVA_DEBITO", "IVA Débito Fiscal", "LIABILITY"),
    ("CMV", "Costo Mercadería Vendida", "EXPENSE"),
    ("INVENTARIO", "Inventario", "ASSET"),
    ("PROVEEDORES", "Proveedores", "LIABILITY"),
    ("GASTOS", "Gastos", "EXPENSE"),
    ("IVA_CREDITO", "IVA Crédito Fiscal", "LIABILITY"),
]


@receiver(post_save, sender=Company)
def create_tax_profile_for_company(sender, instance, created, **kwargs):
    """
    Garantiza que cada compañía tenga un único perfil fiscal.
    Si la compañía es nueva, se crea automáticamente el CompanyProfile.
    Si ya existe, no se duplica gracias al UniqueConstraint.
    """
    if created:
        CompanyProfile.objects.get_or_create(company=instance)

        for code, name, account_type in DEFAULT_ACCOUNT_CODES:
            Account.objects.get_or_create(
                company=instance,
                code=code,
                defaults={
                    "name": name,
                    "account_type": account_type,
                },
            )

        year = date.today().year
        fiscal_year, _ = FiscalYear.objects.get_or_create(
            company=instance,
            year=year,
            defaults={
                "start_date": date(year, 1, 1),
                "end_date": date(year, 12, 31),
                "status": "OPEN",
            },
        )

        for month in range(1, 13):
            start = date(year, month, 1)
            if month in (1, 3, 5, 7, 8, 10, 12):
                end = date(year, month, 31)
            elif month in (4, 6, 9, 11):
                end = date(year, month, 30)
            else:
                end = date(year, month, 29 if year % 4 == 0 else 28)

            Period.objects.get_or_create(
                fiscal_year=fiscal_year,
                month=month,
                defaults={
                    "start_date": start,
                    "end_date": end,
                    "status": "OPEN",
                },
            )
