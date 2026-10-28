from django.core.management.base import BaseCommand

from company.models import Company

from payroll.models import (
    LaborAgreement,
    JobCategory,
    SalaryConcept,
)


class Command(BaseCommand):

    help = "Load payroll master data"

    def handle(self, *args, **kwargs):

        company = Company.objects.first()

        if not company:

            self.stdout.write(
                self.style.ERROR(
                    "No Company found."
                )
            )
            return

        agreement, _ = LaborAgreement.objects.get_or_create(
            company=company,
            code="130/75",
            defaults={
                "name": "Comercio",
                "union_name": "FAECYS",
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Agreement: {agreement}"
            )
        )

        categories = [

            (
                "ADM_A",
                "Administrativo A",
                1200000,
            ),

            (
                "ADM_B",
                "Administrativo B",
                1500000,
            ),

            (
                "SUP",
                "Supervisor",
                2000000,
            ),
        ]

        for code, name, salary in categories:

            JobCategory.objects.get_or_create(
                agreement=agreement,
                code=code,
                defaults={
                    "name": name,
                    "base_salary": salary,
                },
            )

        concepts = [

            (
                "001",
                "Basic Salary",
                "EARNING",
            ),

            (
                "002",
                "Seniority",
                "EARNING",
            ),

            (
                "003",
                "Attendance Bonus",
                "EARNING",
            ),

            (
                "010",
                "Overtime 50%",
                "EARNING",
            ),

            (
                "011",
                "Overtime 100%",
                "EARNING",
            ),

            (
                "101",
                "Retirement Contribution",
                "EMPLOYEE_CONTRIBUTION",
            ),

            (
                "102",
                "INSSJP",
                "EMPLOYEE_CONTRIBUTION",
            ),

            (
                "103",
                "Health Insurance",
                "EMPLOYEE_CONTRIBUTION",
            ),

            (
                "201",
                "Employer Retirement",
                "EMPLOYER_CONTRIBUTION",
            ),

            (
                "202",
                "Employer Health Insurance",
                "EMPLOYER_CONTRIBUTION",
            ),

            (
                "203",
                "ART",
                "EMPLOYER_CONTRIBUTION",
            ),
        ]

        for code, name, concept_type in concepts:

            SalaryConcept.objects.get_or_create(
                company=company,
                code=code,
                defaults={
                    "name": name,
                    "concept_type": concept_type,
                    "calculation_type": "FIXED_AMOUNT",
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Payroll seed completed."
            )
        )