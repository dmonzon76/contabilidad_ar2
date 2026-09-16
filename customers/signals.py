from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import Customer


@receiver(post_save, sender=Customer)
def sync_customer_to_sales(sender, instance, **kwargs):
    sales_customer = apps.get_model("sales", "Customer")
    sales_customer.objects.update_or_create(
        company_id=instance.company_id,
        name=instance.name,
        defaults={
            "tax_id": instance.tax_id,
            "email": instance.email,
            "phone": instance.phone,
            "address": instance.address,
            "is_active": instance.is_active,
        },
    )
