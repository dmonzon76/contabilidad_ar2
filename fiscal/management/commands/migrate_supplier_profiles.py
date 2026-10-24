from django.core.management.base import BaseCommand
from django.db import transaction

from fiscal.models import ThirdPartyTaxProfile
from suppliers.models import Supplier


class Command(BaseCommand):

    help = (
        "Creates one fiscal profile per supplier "
        "based on the current shared profile."
    )

    @transaction.atomic
    def handle(self, *args, **options):

        created = 0
        skipped = 0

        suppliers = (
            Supplier.objects
            .select_related("tax_profile")
            .order_by("name")
        )

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write("MIGRATE SUPPLIER PROFILES")
        self.stdout.write("=" * 60)

        for supplier in suppliers:

            old_profile = supplier.tax_profile

            if not old_profile:

                self.stdout.write(
                    self.style.WARNING(
                        f"SKIPPED: {supplier.name} "
                        f"(no tax profile)"
                    )
                )

                skipped += 1
                continue

            existing_profile = (
                ThirdPartyTaxProfile.objects
                .filter(supplier=supplier)
                .first()
            )

            if existing_profile:

                self.stdout.write(
                    self.style.WARNING(
                        f"SKIPPED: {supplier.name} "
                        f"(profile already exists)"
                    )
                )

                skipped += 1
                continue

            new_profile = (
                ThirdPartyTaxProfile.objects.create(
                    supplier=supplier,
                    company=supplier.company,
                    name=supplier.name,
                    afip_category=old_profile.afip_category,
                    iibb_status=old_profile.iibb_status,
                    is_active=old_profile.is_active,
                    notes=old_profile.notes,
                    multilateral_number=(
                        old_profile.multilateral_number
                    ),
                    has_multilateral_agreement=(
                        old_profile.has_multilateral_agreement
                    ),
                )
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"CREATED: "
                    f"{new_profile.name}"
                )
            )

            created += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Completed. "
                f"Created={created} "
                f"Skipped={skipped}"
            )
        )