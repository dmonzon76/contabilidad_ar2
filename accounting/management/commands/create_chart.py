from django.core.management.base import BaseCommand
from accounting.models import Account
from company.models import Company


PLAN = [
    ("1", "Assets"),
    ("1.1", "Current Assets"),
    ("1.1.1", "Cash"),
    ("1.1.2", "Banks"),
    ("1.1.3", "Accounts Receivable"),
    ("1.2", "Non-current Assets"),
    ("1.2.1", "Property, Plant and Equipment"),

    ("2", "Liabilities"),
    ("2.1", "Current Liabilities"),
    ("2.1.1", "Suppliers"),
    ("2.1.2", "Short-term Loans"),
    ("2.2", "Non-current Liabilities"),
    ("2.2.1", "Long-term Loans"),

    ("3", "Equity"),
    ("3.1", "Capital Stock"),
    ("3.2", "Retained Earnings"),

    ("4", "Income"),
    ("4.1", "Sales"),
    ("4.2", "Financial Income"),

    ("5", "Cost of Sales"),
    ("5.1", "Purchases"),
    ("5.2", "Inventory Variation"),

    ("6", "Expenses"),
    ("6.1", "Administrative Expenses"),
    ("6.2", "Selling Expenses"),
    ("6.3", "Financial Expenses"),
]


class Command(BaseCommand):
    help = "Create a full chart of accounts for a company"

    def add_arguments(self, parser):
        parser.add_argument("company_id", type=int)

    def handle(self, *args, **options):
        company_id = options["company_id"]
        company = Company.objects.get(id=company_id)

        self.stdout.write(self.style.SUCCESS(f"Creating chart of accounts for {company.name}"))

        for code, name in PLAN:
            parent_code = ".".join(code.split(".")[:-1]) if "." in code else None

            parent = None
            if parent_code:
                parent = Account.objects.filter(company=company, code=parent_code).first()

            Account.objects.get_or_create(
                company=company,
                code=code,
                defaults={
                    "name": name,
                    "parent": parent,
                }
            )

        self.stdout.write(self.style.SUCCESS("Chart of accounts created successfully"))

