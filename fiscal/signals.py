from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounting.models import FiscalYear, Period
from accounting.services import AccountingService
from company.models import Company
from fiscal.models.company_profile import CompanyProfile
from fiscal.models import CompanyTaxProfile

@receiver(post_save, sender=Company)
def create_tax_profile_for_company(sender, instance, created, **kwargs):
    if created:
        # ❌ Se elimina esta línea obsoleta:
        # AccountingService.ensure_required_accounts(instance)

        # Se crea únicamente el perfil fiscal de la empresa:
        CompanyTaxProfile.objects.get_or_create(company=instance)
