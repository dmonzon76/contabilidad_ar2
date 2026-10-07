from calendar import monthrange
from datetime import date

from accounting.models import FiscalYear, Period


class FiscalYearService:
    @staticmethod
    def create_year(company, year):

        fiscal_year, created = FiscalYear.objects.get_or_create(
            company=company,
            year=year,
            defaults={
                "start_date": date(year, 1, 1),
                "end_date": date(year, 12, 31),
                "status": "OPEN",
            },
        )

        for month in range(1, 13):
            start_date = date(year, month, 1)

            end_date = date(
                year,
                month,
                monthrange(year, month)[1],
            )

            Period.objects.get_or_create(
                fiscal_year=fiscal_year,
                month=month,
                defaults={
                    "start_date": start_date,
                    "end_date": end_date,
                    "status": "OPEN",
                },
            )

        return fiscal_year
