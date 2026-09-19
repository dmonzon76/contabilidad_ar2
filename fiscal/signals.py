from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounting.models import FiscalYear, Period
from accounting.services import AccountingService
from company.models import Company
from fiscal.models.company_profile import CompanyProfile


@receiver(post_save, sender=Company)
def create_tax_profile_for_company(sender, instance, created, **kwargs):
    """
    Garantiza que cada compañía tenga un único perfil fiscal.
    Si la compañía es nueva, se crea automáticamente el CompanyProfile.
    Si ya existe, no se duplica gracias al UniqueConstraint.
    """
    if created:
        CompanyProfile.objects.get_or_create(company=instance)
        AccountingService.ensure_required_accounts(instance)

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
