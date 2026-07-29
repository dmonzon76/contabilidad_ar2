from django.core.management.base import BaseCommand
from fiscal.models import AFIPActivity
from pathlib import Path


class Command(BaseCommand):
    help = "Importa actividades AFIP desde un archivo TXT oficial separado por ';'"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Ruta al archivo TXT de actividades AFIP",
        )

    def handle(self, *args, **options):
        file_path = Path(options["file"])

        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f"Archivo no encontrado: {file_path}"))
            return

        actividades = []

        with open(file_path, "r", encoding="utf-8") as f:
            next(f)  # saltar cabecera
            for line in f:
                parts = line.strip().split(";")
                if len(parts) >= 3:
                    actividades.append(
                        AFIPActivity(
                            code=parts[0].strip(),
                            description=parts[1].strip(),
                            description_long=parts[2].strip(),
                        )
                    )

        AFIPActivity.objects.all().delete()
        AFIPActivity.objects.bulk_create(actividades)

        self.stdout.write(
            self.style.SUCCESS(f"Importadas {len(actividades)} actividades AFIP.")
        )
