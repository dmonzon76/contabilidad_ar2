from typing import Self

from django.apps import apps
from django.core.management.base import BaseCommand

from fiscal.models import (
    JurisdictionCoefficient,
    TaxRegime,
    TaxRegistryImport,
    ThirdPartyTaxProfile,
    ThirdPartyTaxRule,
)

TaxJurisdiction = apps.get_model("fiscal", "TaxJurisdiction")


class Command(BaseCommand):

    help = "Fiscal module audit"

    def handle(self, *args, **options):

        self.print_header()

        self.audit_counts()

        self.audit_profiles()

        self.audit_unused_regimes()

        self.audit_unused_jurisdictions()

        self.audit_coefficients()

        self.audit_registries()


    def print_header(self):

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write("FISCAL MODULE AUDIT")
        self.stdout.write("=" * 60)

    def audit_counts(self):

        self.stdout.write("")
        self.stdout.write("MASTER DATA")
        self.stdout.write("-" * 60)

        self.stdout.write(
            f"Tax Jurisdictions: "
            f"{TaxJurisdiction.objects.count()}"
        )

        self.stdout.write(
            f"Tax Regimes: "
            f"{TaxRegime.objects.count()}"
        )

        self.stdout.write(
            f"Tax Profiles: "
            f"{ThirdPartyTaxProfile.objects.count()}"
        )

        self.stdout.write(
            f"Tax Rules: "
            f"{ThirdPartyTaxRule.objects.count()}"
        )

        self.stdout.write(
            f"Jurisdiction Coefficients: "
            f"{JurisdictionCoefficient.objects.count()}"
        )

    def audit_profiles(self):

        self.stdout.write("")
        self.stdout.write("PROFILE ANALYSIS")
        self.stdout.write("-" * 60)

        profiles = (
            ThirdPartyTaxProfile.objects
            .prefetch_related(
                "rules",
                "rules__regime",
            )
            .order_by("name")
        )

        if not profiles.exists():

            self.stdout.write(
                self.style.WARNING(
                    "No fiscal profiles found."
                )
            )
            return

        for profile in profiles:

            rules_count = profile.rules.count()

            self.stdout.write("")
            self.stdout.write(
                f"[{profile.id}] {profile.name}"
            )

            self.stdout.write(
                f"AFIP: "
                f"{profile.get_afip_category_display()}"
            )

            self.stdout.write(
                f"IIBB: "
                f"{profile.get_iibb_status_display()}"
            )

            self.stdout.write(
                f"Rules: {rules_count}"
            )

            if (
                profile.has_multilateral_agreement
                and not profile.multilateral_number
            ):
                self.stdout.write(
                    self.style.WARNING(
                        "WARNING: CM enabled without CM number."
                    )
                )

            if rules_count == 0:

                self.stdout.write(
                    self.style.WARNING(
                        "WARNING: Profile without tax rules."
                    )
                )

            else:

                for rule in profile.rules.all():

                    self.stdout.write(
                        f"   - {rule.regime.code}"
                        f" ({rule.effective_rate()}%)"
                    )

    def audit_unused_regimes(self):

        self.stdout.write("")
        self.stdout.write("REGIMES WITHOUT USAGE")
        self.stdout.write("-" * 60)

        unused = (
            TaxRegime.objects
            .filter(
                third_party_rules__isnull=True
            )
            .order_by("name")
        )

        if not unused.exists():

            self.stdout.write(
                self.style.SUCCESS(
                    "All regimes are being used."
                )
            )
            return

        for regime in unused:

            self.stdout.write(
                self.style.WARNING(
                    f"{regime.code} - {regime.name}"
                )
            )

    def audit_unused_jurisdictions(self):

        self.stdout.write("")
        self.stdout.write("JURISDICTIONS WITHOUT REGIMES")
        self.stdout.write("-" * 60)

        unused = (
            TaxJurisdiction.objects
            .filter(
                regimes__isnull=True
            )
            .order_by("name")
        )

        if not unused.exists():

            self.stdout.write(
                self.style.SUCCESS(
                    "All jurisdictions have regimes."
                )
            )
            return

        for jurisdiction in unused:

            self.stdout.write(
                self.style.WARNING(
                    f"{jurisdiction.code} "
                    f"- {jurisdiction.name}"
                )
            )

    def audit_coefficients(self):

        self.stdout.write("")
        self.stdout.write("MULTILATERAL AGREEMENT")
        self.stdout.write("-" * 60)

        multilateral_profiles = (
            ThirdPartyTaxProfile.objects
            .filter(
                has_multilateral_agreement=True
            )
        )

        if not multilateral_profiles.exists():

            self.stdout.write(
                "No multilateral taxpayers found."
            )
            return

        for profile in multilateral_profiles:

            count = (
                JurisdictionCoefficient.objects
                .filter(
                    tax_profile=profile
                )
                .count()
            )

            if count == 0:

                self.stdout.write(
                    self.style.WARNING(
                        f"{profile.name}: "
                        f"no coefficients loaded."
                    )
                )

            else:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"{profile.name}: "
                        f"{count} coefficients loaded."
                    )
                )

    def audit_registries(self):

        self.stdout.write("")
        self.stdout.write(
            "TAX REGISTRIES"
        )
        self.stdout.write(
            "-" * 60
        )

        imports = (
            TaxRegistryImport.objects
            .order_by(
                "-period"
            )
        )

        if not imports.exists():

            self.stdout.write(
                self.style.WARNING(
                    "No registries imported."
                )
            )

            return

        for registry in imports:

            self.stdout.write(
                f"{registry.registry_type}"
            )

            self.stdout.write(
                f"  Period: "
                f"{registry.period}"
            )

            self.stdout.write(
                f"  Records: "
                f"{registry.records_count}"
            )

            self.stdout.write("")