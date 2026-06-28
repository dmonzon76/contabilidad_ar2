from django.core.management.base import BaseCommand
from pathlib import Path
from fiscal.models import AFIPActivity

class Command(BaseCommand):
    help = "Import AFIP activities from the official TXT file"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        input_file = base_dir / "tools" / "ACTIVIDADES_ECONOMICAS_F883.txt"

        if not input_file.exists():
            self.stdout.write(self.style.ERROR(f"TXT file not found: {input_file}"))
            return

        actividades = []
        with open(input_file, "r", encoding="utf-8") as f:
            next(f)  # skip header
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(";")
                if len(parts) < 3:
                    continue

                code = parts[0].strip()
                description = parts[1].strip()
                description_long = parts[2].strip()

                actividades.append((code, description, description_long))

        # Insert into DB
        count = 0
        for code, desc, desc_long in actividades:
            AFIPActivity.objects.update_or_create(
                code=code,
                defaults={
                    "description": desc,
                    "description_long": desc_long,
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {count} AFIP activities."))

