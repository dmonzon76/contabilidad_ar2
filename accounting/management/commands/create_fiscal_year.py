from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from accounting.models.period import FiscalYear, Period
from company.models import Company


class Command(BaseCommand):
    help = "Create a fiscal year and its 12 periods"

    def add_arguments(self, parser):
        parser.add_argument("company_id", type=int)
        parser.add_argument("year", type=int)

    def handle(self, *args, **options):
        company_id = options["company_id"]
        year = options["year"]

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR("Company not found"))
            return

        fy, created = FiscalYear.objects.get_or_create(
            company=company,
            year=year,
            defaults={
                "start_date": date(year, 1, 1),
                "end_date": date(year, 12, 31),
                "status": "OPEN",
            },
        )

        if not created:
            self.stdout.write(self.style.WARNING("Fiscal year already exists"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Fiscal year {year} created"))

        # Create periods
        for month in range(1, 13):
            start = date(year, month, 1)
            if month == 12:
                end = date(year, 12, 31)
            else:
                end = date(year, month + 1, 1) - timezone.timedelta(days=1)

            Period.objects.get_or_create(
                fiscal_year=fy,
                month=month,
                defaults={
                    "start_date": start,
                    "end_date": end,
                    "status": "OPEN",
                },
            )

        self.stdout.write(self.style.SUCCESS("12 periods created or already existed"))
