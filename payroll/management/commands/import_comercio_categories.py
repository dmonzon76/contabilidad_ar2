from django.core.management.base import BaseCommand

from payroll.models import (
    LaborAgreement,
    JobCategory,
)


class Command(BaseCommand):

    help = (
        "Import real Commerce 130/75 categories"
    )

    CATEGORIES = [

        ("MAE_A", "Maestranza A"),
        ("MAE_B", "Maestranza B"),
        ("MAE_C", "Maestranza C"),

        ("ADM_A", "Administrativo A"),
        ("ADM_B", "Administrativo B"),
        ("ADM_C", "Administrativo C"),
        ("ADM_D", "Administrativo D"),
        ("ADM_E", "Administrativo E"),
        ("ADM_F", "Administrativo F"),

        ("CAJ_A", "Cajeros A"),
        ("CAJ_B", "Cajeros B"),
        ("CAJ_C", "Cajeros C"),

        ("PA_A", "Personal Auxiliar A"),
        ("PA_B", "Personal Auxiliar B"),
        ("PA_C", "Personal Auxiliar C"),

        ("AE_A", "Auxiliar Especializado A"),
        ("AE_B", "Auxiliar Especializado B"),
        ("AE_C", "Auxiliar Especializado C"),

        ("VEN_A", "Vendedores A"),
        ("VEN_B", "Vendedores B"),
        ("VEN_C", "Vendedores C"),
        ("VEN_D", "Vendedores D"),
    ]

    def handle(
        self,
        *args,
        **kwargs,
    ):

        agreement = (
            LaborAgreement.objects.get(
                code="130/75"
            )
        )

        created = 0

        for code, name in self.CATEGORIES:

            _, was_created = (
                JobCategory.objects.get_or_create(
                    agreement=agreement,
                    code=code,
                    defaults={
                        "name": name,
                        "base_salary": 0,
                        "is_active": True,
                    },
                )
            )

            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    f"Categories created: "
                    f"{created}"
                )
            )
        )

        self.stdout.write(
            (
                f"Total categories: "
                f"{JobCategory.objects.count()}"
            )
        )