from django.core.management.base import BaseCommand
from accounting.models import Account
from company.models import Company
PLAN_FULL = [
    # code, name, parent_code, account_type

    # --- ASSETS ---
    ("1", "Assets", None, "ASSET"),
    ("1.1", "Current Assets", "1", "ASSET"),
    ("1.1.1", "Cash", "1.1", "ASSET"),
    ("1.1.2", "Banks", "1.1", "ASSET"),
    ("1.1.3", "Checks to be deposited", "1.1", "ASSET"),
    ("1.1.4", "Credit Cards - Pending Settlement", "1.1", "ASSET"),
    ("1.1.5", "Customers", "1.1", "ASSET"),
    ("1.1.6", "Other Receivables", "1.1", "ASSET"),
    ("1.1.7", "Advances to Suppliers", "1.1", "ASSET"),
    ("1.1.8", "Inventory", "1.1", "ASSET"),

    ("1.2", "Non-current Assets", "1", "ASSET"),
    ("1.2.1", "Property, Plant & Equipment", "1.2", "ASSET"),
    ("1.2.2", "Intangible Assets", "1.2", "ASSET"),
    ("1.2.3", "Deferred Tax Assets", "1.2", "ASSET"),

    # --- LIABILITIES ---
    ("2", "Liabilities", None, "LIABILITY"),
    ("2.1", "Current Liabilities", "2", "LIABILITY"),
    ("2.1.1", "Suppliers", "2.1", "LIABILITY"),
    ("2.1.2", "Salaries Payable", "2.1", "LIABILITY"),
    ("2.1.3", "Social Security Payable", "2.1", "LIABILITY"),
    ("2.1.4", "Loans - Short Term", "2.1", "LIABILITY"),
    ("2.1.5", "Credit Cards Payable", "2.1", "LIABILITY"),
    ("2.1.6", "Taxes Payable", "2.1", "LIABILITY"),

    ("2.2", "Non-current Liabilities", "2", "LIABILITY"),
    ("2.2.1", "Loans - Long Term", "2.2", "LIABILITY"),

    # --- EQUITY ---
    ("3", "Equity", None, "EQUITY"),
    ("3.1", "Capital Stock", "3", "EQUITY"),
    ("3.2", "Retained Earnings", "3", "EQUITY"),
    ("3.3", "Legal Reserve", "3", "EQUITY"),
    ("3.4", "Inflation Adjustment", "3", "EQUITY"),

    # --- INCOME ---
    ("4", "Income", None, "INCOME"),
    ("4.1", "Sales", "4", "INCOME"),
    ("4.2", "Other Income", "4", "INCOME"),

    # --- EXPENSES ---
    ("5", "Expenses", None, "EXPENSE"),
    ("5.1", "Administrative Expenses", "5", "EXPENSE"),
    ("5.1.1", "Office Supplies", "5.1", "EXPENSE"),
    ("5.1.2", "Services", "5.1", "EXPENSE"),
    ("5.1.3", "Rent", "5.1", "EXPENSE"),
    ("5.1.4", "Professional Fees", "5.1", "EXPENSE"),
    ("5.2", "Selling Expenses", "5", "EXPENSE"),
    ("5.3", "Financial Expenses", "5", "EXPENSE"),

    # --- AFIP TAXES ---
    ("6", "AFIP Taxes", None, "LIABILITY"),

    # IVA
    ("6.1", "IVA", "6", "LIABILITY"),
    ("6.1.1", "IVA Debit Fiscal", "6.1", "LIABILITY"),
    ("6.1.2", "IVA Credit Fiscal", "6.1", "ASSET"),
    ("6.1.3", "IVA Non-taxable", "6.1", "LIABILITY"),
    ("6.1.4", "IVA Exempt", "6.1", "LIABILITY"),
    ("6.1.5", "IVA Perceptions", "6.1", "ASSET"),
    ("6.1.6", "IVA Retentions", "6.1", "LIABILITY"),

    # Income Tax
    ("6.2", "Income Tax", "6", "LIABILITY"),
    ("6.2.1", "Income Tax Retentions (RG 830)", "6.2", "LIABILITY"),
    ("6.2.2", "Income Tax Perceptions", "6.2", "ASSET"),

    # SUSS
    ("6.3", "SUSS", "6", "LIABILITY"),
    ("6.3.1", "SUSS Retentions", "6.3", "LIABILITY"),

    # Gross Income Tax
    ("6.4", "Gross Income Tax", "6", "LIABILITY"),
    ("6.4.1", "IIBB Perceptions", "6.4", "ASSET"),
    ("6.4.2", "IIBB Retentions", "6.4", "LIABILITY"),

    # PAIS
    ("6.5", "PAIS Tax", "6", "LIABILITY"),
    ("6.5.1", "PAIS Tax", "6.5", "LIABILITY"),
    ("6.5.2", "PAIS Perception", "6.5", "ASSET"),

    # RG 4815
    ("6.6", "Perception RG 4815", "6", "ASSET"),
    ("6.6.1", "Perception RG 4815", "6.6", "ASSET"),

    # Bank Tax (IDyC)
    ("6.7", "Bank Tax (IDyC)", "6", "EXPENSE"),
    ("6.7.1", "Debits Tax", "6.7", "EXPENSE"),
    ("6.7.2", "Credits Tax", "6.7", "EXPENSE"),

    # --- OTHER TAXES ---
    ("8", "Other Taxes", None, "LIABILITY"),
    ("8.1", "Municipal Taxes", "8", "LIABILITY"),
    ("8.2", "Stamp Tax", "8", "LIABILITY"),
    ("8.3", "Personal Assets Tax", "8", "LIABILITY"),

    # --- RESULTS ---
    ("9", "Results", None, "INCOME"),
    ("9.1", "Financial Results", "9", "INCOME"),
    ("9.2", "Inflation Adjustment Results", "9", "INCOME"),
]


class Command(BaseCommand):
    help = "Load FULL AFIP chart of accounts for a company"

    def add_arguments(self, parser):
        parser.add_argument("company_id", type=int)

    def handle(self, *args, **kwargs):
        company_id = kwargs["company_id"]

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR("Company not found"))
            return

        created = 0

        for code, name, parent_code, account_type in PLAN_FULL:
            parent = (
                Account.objects.filter(company=company, code=parent_code).first()
                if parent_code
                else None
            )

            account, was_created = Account.objects.get_or_create(
                company=company,
                code=code,
                defaults={
                    "name": name,
                    "parent": parent,
                    "account_type": account_type,
                    "is_active": True,
                },
            )

            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"FULL AFIP chart loaded for company {company_id}. New accounts: {created}"
            )
        )
