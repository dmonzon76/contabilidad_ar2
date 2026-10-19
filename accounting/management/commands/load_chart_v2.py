from django.core.management.base import BaseCommand

from accounting.models import Account
from company.models import Company

    # =====================================================
    # 1. ASSETS
    # =====================================================
PLAN = [
    ("1", "Assets", "ASSET", None),

    ("1.1", "Current Assets", "ASSET", "1"),

    ("1.1.01", "Cash", "ASSET", "1.1"),
    ("1.1.02", "Banks", "ASSET", "1.1"),
    ("1.1.03", "Checks to Deposit", "ASSET", "1.1"),
    ("1.1.04", "Accounts Receivable", "ASSET", "1.1"),
    ("1.1.05", "Other Receivables", "ASSET", "1.1"),
    ("1.1.06", "Advances to Suppliers", "ASSET", "1.1"),

    ("1.1.07", "VAT Credit Fiscal", "ASSET", "1.1"),
    ("1.1.08", "VAT Perceptions", "ASSET", "1.1"),
    ("1.1.09", "Gross Income Tax Perceptions", "ASSET", "1.1"),
    ("1.1.10", "Income Tax Retentions", "ASSET", "1.1"),

    ("1.1.11", "Merchandise Inventory", "ASSET", "1.1"),
    ("1.1.12", "Raw Materials Inventory", "ASSET", "1.1"),
    ("1.1.13", "Finished Goods Inventory", "ASSET", "1.1"),

    # -----------------------------------------------------

    ("1.2", "Non Current Assets", "ASSET", "1"),

    ("1.2.01", "Property Plant and Equipment", "ASSET", "1.2"),

    ("1.2.01.01", "Land", "ASSET", "1.2.01"),
    ("1.2.01.02", "Buildings", "ASSET", "1.2.01"),
    ("1.2.01.03", "Facilities", "ASSET", "1.2.01"),
    ("1.2.01.04", "Furniture and Fixtures", "ASSET", "1.2.01"),
    ("1.2.01.05", "Computer Equipment", "ASSET", "1.2.01"),
    ("1.2.01.06", "Vehicles", "ASSET", "1.2.01"),

    # Accumulated Depreciation (contra-assets)

    ("1.2.02", "Accumulated Depreciation", "ASSET", "1.2"),

    ("1.2.02.01", "Accumulated Depreciation - Buildings", "ASSET", "1.2.02"),
    ("1.2.02.02", "Accumulated Depreciation - Facilities", "ASSET", "1.2.02"),
    ("1.2.02.03", "Accumulated Depreciation - Furniture and Fixtures", "ASSET", "1.2.02"),
    ("1.2.02.04", "Accumulated Depreciation - Computer Equipment", "ASSET", "1.2.02"),
    ("1.2.02.05", "Accumulated Depreciation - Vehicles", "ASSET", "1.2.02"),

    ("1.2.03", "Intangible Assets", "ASSET", "1.2"),

    ("1.2.03.01", "Software Licenses", "ASSET", "1.2.03"),
    ("1.2.03.02", "Trademarks", "ASSET", "1.2.03"),
    ("1.2.03.03", "Patents", "ASSET", "1.2.03"),

    # =====================================================
    # 2. LIABILITIES
    # =====================================================

    ("2", "Liabilities", "LIABILITY", None),

    ("2.1", "Current Liabilities", "LIABILITY", "2"),

    ("2.1.01", "Suppliers", "LIABILITY", "2.1"),
    ("2.1.02", "Foreign Suppliers", "LIABILITY", "2.1"),
    ("2.1.03", "Salaries Payable", "LIABILITY", "2.1"),
    ("2.1.04", "Social Security Payable", "LIABILITY", "2.1"),

    ("2.1.05", "VAT Debit Fiscal", "LIABILITY", "2.1"),
    ("2.1.06", "VAT Payable", "LIABILITY", "2.1"),

    ("2.1.07", "VAT Perceptions Payable", "LIABILITY", "2.1"),
    ("2.1.08", "Gross Income Tax Payable", "LIABILITY", "2.1"),
    ("2.1.09", "Tax Retentions Payable", "LIABILITY", "2.1"),

    ("2.1.10", "Customer Advances", "LIABILITY", "2.1"),
    ("2.1.11", "Short Term Bank Loans", "LIABILITY", "2.1"),

    ("2.2", "Non Current Liabilities", "LIABILITY", "2"),

    ("2.2.01", "Long Term Loans", "LIABILITY", "2.2"),
    ("2.2.02", "Long Term Financial Debt", "LIABILITY", "2.2"),

    # =====================================================
    # 3. EQUITY
    # =====================================================

    ("3", "Equity", "EQUITY", None),

    ("3.1", "Share Capital", "EQUITY", "3"),
    ("3.2", "Capital Adjustments", "EQUITY", "3"),
    ("3.3", "Legal Reserves", "EQUITY", "3"),
    ("3.4", "Retained Earnings", "EQUITY", "3"),
    ("3.5", "Current Year Result", "EQUITY", "3"),

    # =====================================================
    # 4. REVENUE
    # =====================================================

    ("4", "Revenue", "INCOME", None),

    ("4.1", "Sales Revenue", "INCOME", "4"),

    ("4.1.01", "Product Sales", "INCOME", "4.1"),
    ("4.1.02", "Service Sales", "INCOME", "4.1"),
    ("4.1.03", "Exempt Sales", "INCOME", "4.1"),
    ("4.1.04", "Non Taxable Sales", "INCOME", "4.1"),
    ("4.1.05", "Export Sales", "INCOME", "4.1"),

    ("4.2", "Other Revenue", "INCOME", "4"),

    ("4.2.01", "Interest Income", "INCOME", "4.2"),
    ("4.2.02", "Foreign Exchange Gain", "INCOME", "4.2"),
    ("4.2.03", "Expense Recoveries", "INCOME", "4.2"),
    ("4.2.04", "Extraordinary Income", "INCOME", "4.2"),

    # =====================================================
    # 5. COST OF SALES
    # =====================================================

    ("5", "Cost of Sales", "EXPENSE", None),

    ("5.1", "Product Costs", "EXPENSE", "5"),

    ("5.1.01", "Cost of Goods Sold", "EXPENSE", "5.1"),
    ("5.1.02", "Raw Materials Cost", "EXPENSE", "5.1"),
    ("5.1.03", "Production Cost", "EXPENSE", "5.1"),
    ("5.1.04", "Inventory Adjustment", "EXPENSE", "5.1"),

    ("5.2", "Service Costs", "EXPENSE", "5"),

    ("5.2.01", "Services Cost", "EXPENSE", "5.2"),
    ("5.2.02", "Subcontracted Services", "EXPENSE", "5.2"),
    ("5.2.03", "Technical Fees", "EXPENSE", "5.2"),

    # =====================================================
    # 6. OPERATING EXPENSES
    # =====================================================

    ("6", "Operating Expenses", "EXPENSE", None),

    ("6.1", "Administrative Expenses", "EXPENSE", "6"),

    ("6.1.01", "Administrative Salaries", "EXPENSE", "6.1"),
    ("6.1.02", "Social Security Expenses", "EXPENSE", "6.1"),
    ("6.1.03", "Utilities", "EXPENSE", "6.1"),
    ("6.1.04", "Rent Expense", "EXPENSE", "6.1"),
    ("6.1.05", "Insurance Expense", "EXPENSE", "6.1"),
    ("6.1.06", "Office Supplies", "EXPENSE", "6.1"),
    ("6.1.07", "Bank Charges", "EXPENSE", "6.1"),
    ("6.1.08", "Professional Fees", "EXPENSE", "6.1"),
    ("6.1.09", "Depreciation Expense", "EXPENSE", "6.1"),
    ("6.1.10", "Amortization Expense", "EXPENSE", "6.1"),

    ("6.2", "Selling Expenses", "EXPENSE", "6"),

    ("6.2.01", "Sales Salaries", "EXPENSE", "6.2"),
    ("6.2.02", "Advertising", "EXPENSE", "6.2"),
    ("6.2.03", "Sales Commissions", "EXPENSE", "6.2"),
    ("6.2.04", "Travel Expenses", "EXPENSE", "6.2"),
    ("6.2.05", "Freight Expense", "EXPENSE", "6.2"),

    ("6.3", "Financial Expenses", "EXPENSE", "6"),

    ("6.3.01", "Interest Expense", "EXPENSE", "6.3"),
    ("6.3.02", "Foreign Exchange Loss", "EXPENSE", "6.3"),
    ("6.3.03", "Other Financial Expenses", "EXPENSE", "6.3"),
]

class Command(BaseCommand):
    help = "Load professional chart of accounts for a company"

    def add_arguments(self, parser):
        parser.add_argument("company_id", type=int)

    def handle(self, *args, **kwargs):
        company_id = kwargs["company_id"]
        company = Company.objects.get(id=company_id)

        self.stdout.write(f"Loading chart of accounts for {company.name}")

        for code, name, acc_type, parent_code in PLAN:
            # Si ya existe → no lo toca
            if Account.objects.filter(company=company, code=code).exists():
                continue

            parent = None
            if parent_code:
                parent = Account.objects.filter(company=company, code=parent_code).first()

            Account.objects.create(
                company=company,
                code=code,
                name=name,
                account_type=acc_type,
                parent=parent,
                is_active=True,
            )

        self.stdout.write(self.style.SUCCESS("Professional chart of accounts loaded successfully"))
