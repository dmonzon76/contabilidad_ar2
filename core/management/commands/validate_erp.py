# core/management/commands/validate_erp.py

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.urls import NoReverseMatch, reverse

from accounting.models import Account, AccountingSettings
from company.models import Company
from customers.models import Customer
from payroll.models import (
    Employee,
    JobCategory,
    LaborAgreement,
    SalaryConcept,
    SalaryScale,
)
from products.models import Product
from suppliers.models import Supplier


class Command(BaseCommand):

    help = "ERP validation and health check"

    def add_arguments(self, parser):

        parser.add_argument(
            "--deep",
            action="store_true",
            help="Run deep validation",
        )

    # -----------------------------------------------------
    # Helpers
    # -----------------------------------------------------

    def ok(self, message):
        self.stdout.write(
            self.style.SUCCESS(
                f"[OK] {message}"
            )
        )

    def warn(self, message):
        self.stdout.write(
            self.style.WARNING(
                f"[WARN] {message}"
            )
        )

    def error(self, message):
        self.stdout.write(
            self.style.ERROR(
                f"[ERROR] {message}"
            )
        )

    # -----------------------------------------------------
    # Main
    # -----------------------------------------------------

    def handle(self, *args, **options):

        self.deep = options["deep"]

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("ERP VALIDATION")
        self.stdout.write("=" * 70)

        self.validate_companies()

        self.validate_master_data()

        self.validate_accounting()

        self.validate_payroll()

        self.validate_urls()

        self.validate_multicompany()

        if self.deep:
            self.deep_validation()

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write(
            self.style.SUCCESS(
                "VALIDATION COMPLETED"
            )
        )
        self.stdout.write("=" * 70)

    # -----------------------------------------------------
    # Basic
    # -----------------------------------------------------

    def validate_companies(self):

        total = Company.objects.count()

        if total:
            self.ok(f"Companies: {total}")
        else:
            self.error("No companies found")

    def validate_master_data(self):

        self.ok(
            f"Customers: {Customer.objects.count()}"
        )

        self.ok(
            f"Suppliers: {Supplier.objects.count()}"
        )

        self.ok(
            f"Products: {Product.objects.count()}"
        )

    def validate_accounting(self):

        self.ok(
            f"Accounts: {Account.objects.count()}"
        )

        settings = AccountingSettings.objects.count()

        if settings:
            self.ok(
                f"Accounting Settings: {settings}"
            )
        else:
            self.warn(
                "AccountingSettings missing for all companies"
            )

    def validate_payroll(self):

        self.ok(
            f"Employees: {Employee.objects.count()}"
        )

        self.ok(
            f"Labor Agreements: {LaborAgreement.objects.count()}"
        )

        self.ok(
            f"Job Categories: {JobCategory.objects.count()}"
        )

        self.ok(
            f"Salary Concepts: {SalaryConcept.objects.count()}"
        )

        self.ok(
            f"Salary Scales: {SalaryScale.objects.count()}"
        )

    def validate_urls(self):

        urls = [

           "main_dashboard",

            "company:company_list",

            "sales:dashboard",

            "purchases:dashboard",

            "inventory:inventory_dashboard",

            "accounting:dashboard",

            "payroll:dashboard",
        ]

        for url in urls:

            try:

                reverse(url)

                self.ok(
                    f"URL: {url}"
                )

            except NoReverseMatch:

                self.error(
                    f"Broken URL: {url}"
                )

    def validate_multicompany(self):

        self.stdout.write("")
        self.stdout.write(
            "MULTI-COMPANY SUMMARY"
        )

        for company in Company.objects.all():

            customers = Customer.objects.filter(
                company=company
            ).count()

            products = Product.objects.filter(
                company=company
            ).count()

            employees = Employee.objects.filter(
                company=company
            ).count()

            accounts = Account.objects.filter(
                company=company
            ).count()

            self.stdout.write("")
            self.stdout.write(company.name)

            self.stdout.write(
                f"  Customers : {customers}"
            )

            self.stdout.write(
                f"  Products  : {products}"
            )

            self.stdout.write(
                f"  Employees : {employees}"
            )

            self.stdout.write(
                f"  Accounts  : {accounts}"
            )

    # -----------------------------------------------------
    # Deep Validation
    # -----------------------------------------------------

    def deep_validation(self):

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("DEEP VALIDATION")
        self.stdout.write("=" * 70)

        self.check_company_integrity()

        self.check_accounting_settings()

        self.check_products()

        self.check_duplicate_products()

        self.check_customers()

        self.check_suppliers()

        self.check_employees()

    # -----------------------------------------------------

    def check_company_integrity(self):

        self.stdout.write("")
        self.stdout.write(
            "COMPANY INTEGRITY"
        )

        for company in Company.objects.all():

            if not company.name:

                self.error(
                    f"Company {company.id} without name"
                )

            else:

                self.ok(
                    f"{company.name}"
                )

    # -----------------------------------------------------

    def check_accounting_settings(self):

        self.stdout.write("")
        self.stdout.write(
            "ACCOUNTING SETTINGS"
        )

        for company in Company.objects.all():

            exists = (
                AccountingSettings.objects
                .filter(company=company)
                .exists()
            )

            if exists:

                self.ok(
                    f"{company.name}"
                )

            else:

                self.error(
                    f"{company.name} missing AccountingSettings"
                )

    # -----------------------------------------------------

    def check_products(self):

        self.stdout.write("")
        self.stdout.write(
            "PRODUCT INTEGRITY"
        )

        no_company = Product.objects.filter(
            company__isnull=True
        ).count()

        if no_company:

            self.error(
                f"Products without company: {no_company}"
            )

        else:

            self.ok(
                "Products company integrity"
            )

        no_income = Product.objects.filter(
            income_account__isnull=True
        ).count()

        if no_income:

            self.warn(
                f"Products without income account: {no_income}"
            )

    # -----------------------------------------------------

    def check_duplicate_products(self):

        self.stdout.write("")
        self.stdout.write(
            "DUPLICATE PRODUCT SKU"
        )

        duplicates = (
            Product.objects
            .values(
                "company",
                "sku",
            )
            .annotate(
                total=Count("id")
            )
            .filter(
                total__gt=1
            )
        )

        if duplicates.exists():

            self.error(
                f"Duplicate SKU groups: {duplicates.count()}"
            )

        else:

            self.ok(
                "SKU uniqueness"
            )

    # -----------------------------------------------------

    def check_customers(self):

        self.stdout.write("")
        self.stdout.write(
            "CUSTOMERS"
        )

        no_company = Customer.objects.filter(
            company__isnull=True
        ).count()

        if no_company:

            self.error(
                f"Customers without company: {no_company}"
            )

        else:

            self.ok(
                "Customer integrity"
            )

    # -----------------------------------------------------

    def check_suppliers(self):

        self.stdout.write("")
        self.stdout.write(
            "SUPPLIERS"
        )

        no_company = Supplier.objects.filter(
            company__isnull=True
        ).count()

        if no_company:

            self.error(
                f"Suppliers without company: {no_company}"
            )

        else:

            self.ok(
                "Supplier integrity"
            )

    # -----------------------------------------------------

    def check_employees(self):

        self.stdout.write("")
        self.stdout.write(
            "EMPLOYEES"
        )

        no_company = Employee.objects.filter(
            company__isnull=True
        ).count()

        if no_company:

            self.error(
                f"Employees without company: {no_company}"
            )

        else:

            self.ok(
                "Employee integrity"
            )