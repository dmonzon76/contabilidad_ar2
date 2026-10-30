from django.core.management.base import BaseCommand

from company.models import Company

from payroll.models import SalaryConcept


class Command(BaseCommand):

    help = (
        "Load Payroll V3 salary concepts"
    )

    def handle(
        self,
        *args,
        **kwargs,
    ):

        company = Company.objects.first()

        if not company:

            self.stdout.write(
                self.style.ERROR(
                    "No Company found."
                )
            )

            return

        concepts = [

            (
                "050",
                "Agreement Fixed Amount",
                "EARNING",
            ),

            (
                "060",
                "Extraordinary Agreement Amount",
                "EARNING",
            ),

        ]

        created = 0
        existing = 0

        for (
            code,
            name,
            concept_type,
        ) in concepts:

            _, was_created = (
                SalaryConcept.objects.get_or_create(
                    company=company,
                    code=code,
                    defaults={
                        "name": name,
                        "concept_type": concept_type,
                        "calculation_type": "FIXED_AMOUNT",
                        "is_active": True,
                    },
                )
            )

            if was_created:

                created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[CREATED] {code} {name}"
                    )
                )

            else:

                existing += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"[EXISTS] {code} {name}"
                    )
                )

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(
            f"Created: {created}"
        )
        self.stdout.write(
            f"Existing: {existing}"
        )
        self.stdout.write("=" * 60)