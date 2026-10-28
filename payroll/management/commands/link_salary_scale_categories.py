from django.core.management.base import BaseCommand

from payroll.models import (
    JobCategory,
    SalaryScaleLine,
)


class Command(BaseCommand):

    help = (
        "Link salary scale lines to payroll categories"
    )

    def add_arguments(
        self,
        parser,
    ):

        parser.add_argument(
            "--dry-run",
            action="store_true",
        )

    def handle(
        self,
        *args,
        **options,
    ):

        dry_run = options["dry_run"]

        linked = 0

        for line in SalaryScaleLine.objects.all():

            full_name = (
                f"{line.group_name} "
                f"{line.category_name}"
            )

            category = (
                JobCategory.objects.filter(
                    name=full_name,
                )
                .first()
            )

            if not category:

                self.stdout.write(
                    self.style.WARNING(
                        f"[NO MATCH] {full_name}"
                    )
                )
                continue

            self.stdout.write(
                f"{full_name} -> {category.name}"
            )

            if not dry_run:

                line.category = category
                line.save(
                    update_fields=["category"]
                )

            linked += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Linked categories: {linked}"
            )
        )