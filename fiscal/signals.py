from django.db.models.signals import post_save
from django.dispatch import receiver

from accounting.services import AccountingService
from company.models import Company
from fiscal.models import CompanyProfile


@receiver(post_save, sender=Company)
def create_tax_profile_for_company(sender, instance, created, **kwargs):
    """
    Crea el perfil fiscal predeterminado al registrar una empresa.
    """
    if created:
        CompanyProfile.objects.get_or_create(company=instance)

        if hasattr(AccountingService, "ensure_required_accounts"):
            AccountingService.ensure_required_accounts(instance)
