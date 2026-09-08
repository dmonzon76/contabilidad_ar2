from django.db.models.signals import post_save
from django.dispatch import receiver
import calendar

from accounting.models import FiscalYear, Period


@receiver(post_save, sender=FiscalYear)
def create_annual_period(sender, instance, created, **kwargs):
    """
    Auto-create the twelve monthly accounting periods for a fiscal year.
    """

    if not created:
        return

    # If the period already exists, do nothing
    if Period.objects.filter(fiscal_year=instance).exists():
        return

    for month in range(1, 13):
        start_date = instance.start_date.replace(month=month, day=1)
        last_day = calendar.monthrange(instance.year, month)[1]
        end_date = instance.end_date.replace(month=month, day=last_day)
        Period.objects.create(
            fiscal_year=instance,
            month=month,
            start_date=start_date,
            end_date=end_date,
            status="OPEN",
        )
