import json
from django.core.management.base import BaseCommand
from fiscal.models import AFIPActivity


class Command(BaseCommand):
    help = "Load AFIP activities from JSON file"

    def handle(self, *args, **kwargs):
        path = "fiscal/data/afip_activities.json"

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            AFIPActivity.objects.all().delete()

            for item in data:
                AFIPActivity.objects.create(
                    code=item["code"],
                    description=item["description"],
                )

            self.stdout.write(self.style.SUCCESS("AFIP activities loaded successfully."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
