from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounting.models import Account, AccountingSettings
from company.models import Company
from customers.models import Customer
from payroll.models import (
    JobCategory,
    LaborAgreement,
    SalaryConcept,
    SalaryScale,
    SalaryScaleLine,
)
from products.models import Product


class Command(BaseCommand):
    help = "Clone master data between companies"

    def add_arguments(self, parser):
        parser.add_argument("--source", type=int, required=True)
        parser.add_argument("--target", type=int, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        source_company = Company.objects.get(pk=options["source"])
        target_company = Company.objects.get(pk=options["target"])

        if source_company.pk == target_company.pk:
            raise CommandError("The source and target company must be different.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Cloning master data from {source_company.name} to {target_company.name}"
            )
        )

        account_map = {}
        source_accounts = Account.objects.filter(company=source_company).select_related("parent").order_by("code")

        for account in source_accounts:
            cloned_account = Account.objects.create(
                company=target_company,
                code=account.code,
                name=account.name,
                parent=None,
                account_type=account.account_type,
                is_active=account.is_active,
            )
            account_map[account.id] = cloned_account

        for account in source_accounts:
            cloned_account = account_map.get(account.id)
            if not cloned_account or not account.parent_id:
                continue

            parent_clone = account_map.get(account.parent_id)
            if parent_clone:
                cloned_account.parent = parent_clone
                cloned_account.save(update_fields=["parent"])

        self.stdout.write(self.style.SUCCESS("✓ Accounts cloned"))

        source_settings = AccountingSettings.objects.filter(company=source_company).first()
        if source_settings:
            settings_data = {
                "company": target_company,
                "account_customers": account_map.get(source_settings.account_customers_id),
                "account_sales_goods": account_map.get(source_settings.account_sales_goods_id),
                "account_sales_services": account_map.get(source_settings.account_sales_services_id),
                "account_iva_debit": account_map.get(source_settings.account_iva_debit_id),
                "account_suppliers": account_map.get(source_settings.account_suppliers_id),
                "account_inventory": account_map.get(source_settings.account_inventory_id),
                "account_expenses": account_map.get(source_settings.account_expenses_id),
                "account_iva_credit": account_map.get(source_settings.account_iva_credit_id),
                "account_cmv": account_map.get(source_settings.account_cmv_id),
                "account_cash": account_map.get(source_settings.account_cash_id),
                "account_bank": account_map.get(source_settings.account_bank_id),
                "account_iva_perception_payable": account_map.get(source_settings.account_iva_perception_payable_id),
                "account_iibb_perception_payable": account_map.get(source_settings.account_iibb_perception_payable_id),
                "account_iva_retention_payable": account_map.get(source_settings.account_iva_retention_payable_id),
                "account_ganancias_retention_payable": account_map.get(source_settings.account_ganancias_retention_payable_id),
                "account_iibb_retention_payable": account_map.get(source_settings.account_iibb_retention_payable_id),
                "account_current_year_result": account_map.get(source_settings.account_current_year_result_id),
            }

            target_settings, created = AccountingSettings.objects.get_or_create(company=target_company)
            for field_name, value in settings_data.items():
                if field_name == "company":
                    continue
                setattr(target_settings, field_name, value)
            target_settings.save()

            self.stdout.write(self.style.SUCCESS("✓ Accounting settings cloned"))

        for customer in Customer.objects.filter(company=source_company):
            Customer.objects.update_or_create(
                company=target_company,
                name=customer.name,
                defaults={
                    "tax_id": customer.tax_id,
                    "email": customer.email,
                    "phone": customer.phone,
                    "address": customer.address,
                    "tax_profile": customer.tax_profile,
                },
            )

        self.stdout.write(self.style.SUCCESS("✓ Customers cloned"))

        for product in Product.objects.filter(company=source_company):
            Product.objects.update_or_create(
                company=target_company,
                sku=product.sku,
                defaults={
                    "name": product.name,
                    "description": product.description,
                    "detail": product.detail,
                    "type": product.type,
                    "income_account": account_map.get(product.income_account_id),
                    "purchase_account": account_map.get(product.purchase_account_id),
                    "tax": product.tax,
                    "price": product.price,
                },
            )

        self.stdout.write(self.style.SUCCESS("✓ Products cloned"))

        agreement_map = {}
        for agreement in LaborAgreement.objects.filter(company=source_company):
            new_agreement, _ = LaborAgreement.objects.update_or_create(
                company=target_company,
                code=agreement.code,
                defaults={
                    "name": agreement.name,
                    "union_name": agreement.union_name,
                    "description": agreement.description,
                    "is_active": agreement.is_active,
                },
            )
            agreement_map[agreement.id] = new_agreement

        self.stdout.write(self.style.SUCCESS("✓ Labor agreements cloned"))

        category_map = {}
        for category in JobCategory.objects.filter(agreement__company=source_company):
            new_category, _ = JobCategory.objects.update_or_create(
                agreement=agreement_map[category.agreement_id],
                code=category.code,
                defaults={
                    "name": category.name,
                    "base_salary": category.base_salary,
                    "description": category.description,
                    "is_active": category.is_active,
                },
            )
            category_map[category.id] = new_category

        self.stdout.write(self.style.SUCCESS("✓ Job categories cloned"))

        for concept in SalaryConcept.objects.filter(company=source_company):
            SalaryConcept.objects.update_or_create(
                company=target_company,
                code=concept.code,
                defaults={
                    "name": concept.name,
                    "concept_type": concept.concept_type,
                    "calculation_type": concept.calculation_type,
                    "default_amount": concept.default_amount,
                    "percentage": concept.percentage,
                    "formula": concept.formula,
                    "is_remunerative": concept.is_remunerative,
                    "affects_sac": concept.affects_sac,
                    "affects_vacation": concept.affects_vacation,
                    "is_active": concept.is_active,
                    "notes": concept.notes,
                },
            )

        self.stdout.write(self.style.SUCCESS("✓ Salary concepts cloned"))

        scale_map = {}
        for scale in SalaryScale.objects.filter(agreement__company=source_company):
            new_scale = SalaryScale.objects.create(
                agreement=agreement_map[scale.agreement_id],
                period=scale.period,
                is_active=scale.is_active,
            )
            scale_map[scale.id] = new_scale

            for line in scale.lines.all():
                SalaryScaleLine.objects.create(
                    scale=new_scale,
                    group_name=line.group_name,
                    category_name=line.category_name,
                    category=category_map.get(line.category_id),
                    basic_salary=line.basic_salary,
                    fixed_amount=line.fixed_amount,
                    extraordinary_amount=line.extraordinary_amount,
                    total_amount=line.total_amount,
                )

        self.stdout.write(self.style.SUCCESS("✓ Salary scales cloned"))

        self.stdout.write(self.style.SUCCESS("Master data cloned successfully."))