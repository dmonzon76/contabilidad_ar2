from django.core.management.base import BaseCommand
from django.db import transaction

from company.models import Company
from payroll.models import (
    JobCategory,
    LaborAgreement,
    SalaryConcept,
)


class Command(BaseCommand):

    help = (
        "Copy payroll setup between companies"
    )

    def add_arguments(
        self,
        parser,
    ):

        parser.add_argument(
            "--source",
            type=int,
            required=True,
        )

        parser.add_argument(
            "--target",
            type=int,
            required=True,
        )

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):

        source_company = Company.objects.get(
            pk=options["source"]
        )

        target_company = Company.objects.get(
            pk=options["target"]
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Copying payroll setup "
                f"from {source_company.name} "
                f"to {target_company.name}"
            )
        )

        agreement_map = {}

        # ---------------------------------
        # Labor Agreements
        # ---------------------------------

        for agreement in (
            LaborAgreement.objects.filter(
                company=source_company
            )
        ):

            new_agreement = (
                LaborAgreement.objects.create(
                    company=target_company,
                    code=agreement.code,
                    name=agreement.name,
                    union_name=agreement.union_name,
                    description=agreement.description,
                    is_active=agreement.is_active,
                )
            )

            agreement_map[
                agreement.id
            ] = new_agreement

        self.stdout.write(
            self.style.SUCCESS(
                "✓ Labor Agreements copied"
            )
        )

        category_map = {}

        # ---------------------------------
        # Job Categories
        # ---------------------------------

        for category in (
            JobCategory.objects.filter(
                agreement__company=source_company
            )
        ):

            new_category = (
                JobCategory.objects.create(
                    agreement=agreement_map[
                        category.agreement_id
                    ],
                    code=category.code,
                    name=category.name,
                    base_salary=category.base_salary,
                    description=category.description,
                    is_active=category.is_active,
                )
            )

            category_map[
                category.id
            ] = new_category

        self.stdout.write(
            self.style.SUCCESS(
                "✓ Job Categories copied"
            )
        )

        # ---------------------------------
        # Salary Concepts
        # ---------------------------------

        for concept in (
            SalaryConcept.objects.filter(
                company=source_company
            )
        ):

            SalaryConcept.objects.create(
                company=target_company,
                code=concept.code,
                name=concept.name,
                concept_type=concept.concept_type,
                calculation_type=concept.calculation_type,
                default_amount=concept.default_amount,
                percentage=concept.percentage,
                formula=concept.formula,
                is_remunerative=concept.is_remunerative,
                affects_sac=concept.affects_sac,
                affects_vacation=concept.affects_vacation,
                is_active=concept.is_active,
                notes=concept.notes,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "✓ Salary Concepts copied"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Payroll setup copied successfully."
            )
        )