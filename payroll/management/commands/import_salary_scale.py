from pathlib import Path

import pandas as pd  # pyright: ignore[reportMissingModuleSource]
from django.core.management.base import BaseCommand

from payroll.models import (
    LaborAgreement,
    SalaryScale,
    SalaryScaleLine,
)


class Command(BaseCommand):

    help = "Import salary scale from Excel"

    def add_arguments(
        self,
        parser,
    ):

        parser.add_argument(
            "file",
            type=str,
        )

        parser.add_argument(
            "--period",
            required=True,
        )

    def handle(
        self,
        *args,
        **options,
    ):

        file_path = Path(
            options["file"]
        )

        period = options["period"]

        agreement = (
            LaborAgreement.objects.get(
                code="130/75"
            )
        )

        scale, _ = (
            SalaryScale.objects.get_or_create(
                agreement=agreement,
                period=period,
            )
        )

        df = pd.read_excel(
            file_path,
            engine="openpyxl",
        )

        SalaryScaleLine.objects.filter(
            scale=scale
        ).delete()

        imported = 0

        for _, row in df.iterrows():

            SalaryScaleLine.objects.create(
                scale=scale,

                group_name=str(
                    row["Grupo"]
                ).strip(),

                category_name=str(
                    row["Categoria"]
                ).strip(),

                basic_salary=row[
                    "Basico"
                ],

                fixed_amount=row[
                    "Suma Fija"
                ],

                extraordinary_amount=row[
                    "Asignacion Extraordinaria"
                ],

                total_amount=row[
                    "Total"
                ],
            )

            imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    f"Salary scale imported. "
                    f"Lines: {imported}"
                )
            )
        )