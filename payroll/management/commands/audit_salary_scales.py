from django.core.management.base import BaseCommand

from payroll.models import (
    SalaryScale,
)


class Command(BaseCommand):

    help = "Audit salary scales"

    def handle(self, *args, **kwargs):

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write("SALARY SCALES")
        self.stdout.write("=" * 60)

        for scale in SalaryScale.objects.all():

            self.stdout.write("")
            self.stdout.write(
                f"Agreement: "
                f"{scale.agreement}"
            )

            self.stdout.write(
                f"Period: "
                f"{scale.period}"
            )

            self.stdout.write(
                f"Lines: "
                f"{scale.lines.count()}"
            )

            self.stdout.write("")

            for line in scale.lines.all():

                self.stdout.write(
                    (
                        f"{line.group_name} "
                        f"{line.category_name} | "
                        f"Basic: {line.basic_salary} | "
                        f"Fixed: {line.fixed_amount} | "
                        f"Total: {line.total_amount}"
                    )
                )