from decimal import Decimal

from django.core.management.base import BaseCommand

from fiscal.models.tax import Tax
from fiscal.models.tax_jurisdiction import TaxJurisdiction
from fiscal.models.tax_regime import TaxRegime


class Command(BaseCommand):

    help = "Carga los regímenes fiscales maestros"

    def handle(self, *args, **options):

        jurisdictions = {
            j.code: j
            for j in TaxJurisdiction.objects.all()
        }

        taxes = {
            t.code: t
            for t in Tax.objects.all()
        }

        regimes = [

            # =====================================================
            # IVA
            # =====================================================

            {
                "code": "IVA_PERC",
                "name": "IVA Percepción AFIP",
                "tax_type": "VAT",
                "application_type": "PERCEPTION",
                "tax_code": "IVA_21",
                "jurisdiction": "AFIP",
                "rate": Decimal("3.0000"),
                "minimum_base": Decimal("0.00"),
            },

            {
                "code": "IVA_RET",
                "name": "IVA Retención AFIP",
                "tax_type": "VAT",
                "application_type": "RETENTION",
                "tax_code": "IVA_21",
                "jurisdiction": "AFIP",
                "rate": Decimal("50.0000"),
                "minimum_base": Decimal("0.00"),
            },

            # =====================================================
            # GANANCIAS
            # =====================================================

            {
                "code": "GAN_RG830",
                "name": "Ganancias RG 830",
                "tax_type": "PROFIT",
                "application_type": "RETENTION",
                "tax_code": "IVA_21",
                "jurisdiction": "AFIP",
                "rate": Decimal("2.0000"),
                "minimum_base": Decimal("0.00"),
            },

            # =====================================================
            # ARBA
            # =====================================================

            {
                "code": "ARBA_PERC",
                "name": "ARBA Percepción",
                "tax_type": "IIBB",
                "application_type": "PERCEPTION",
                "tax_code": "IVA_21",
                "jurisdiction": "ARBA",
                "rate": Decimal("3.5000"),
                "minimum_base": Decimal("0.00"),
            },

            {
                "code": "ARBA_RET",
                "name": "ARBA Retención",
                "tax_type": "IIBB",
                "application_type": "RETENTION",
                "tax_code": "IVA_21",
                "jurisdiction": "ARBA",
                "rate": Decimal("2.5000"),
                "minimum_base": Decimal("0.00"),
            },

            # =====================================================
            # AGIP
            # =====================================================

            {
                "code": "AGIP_PERC",
                "name": "AGIP Percepción",
                "tax_type": "IIBB",
                "application_type": "PERCEPTION",
                "tax_code": "IVA_21",
                "jurisdiction": "AGIP",
                "rate": Decimal("2.0000"),
                "minimum_base": Decimal("0.00"),
            },

            {
                "code": "AGIP_RET",
                "name": "AGIP Retención",
                "tax_type": "IIBB",
                "application_type": "RETENTION",
                "tax_code": "IVA_21",
                "jurisdiction": "AGIP",
                "rate": Decimal("1.7500"),
                "minimum_base": Decimal("0.00"),
            },

            # =====================================================
            # SIRCREB
            # =====================================================

            {
                "code": "SIRCREB",
                "name": "SIRCREB",
                "tax_type": "IIBB",
                "application_type": "RETENTION",
                "tax_code": "IVA_21",
                "jurisdiction": "SIRCREB",
                "rate": Decimal("1.0000"),
                "minimum_base": Decimal("0.00"),
            },

            # =====================================================
            # SUSS
            # =====================================================

            {
                "code": "SUSS_RET",
                "name": "SUSS",
                "tax_type": "SUSS",
                "application_type": "RETENTION",
                "tax_code": "IVA_21",
                "jurisdiction": "AFIP",
                "rate": Decimal("1.0000"),
                "minimum_base": Decimal("0.00"),
            },
        ]

        created = 0
        updated = 0

        for item in regimes:

            tax = taxes.get(item["tax_code"])

            if not tax:
                self.stdout.write(
                    self.style.WARNING(
                        f"Tax not found: {item['tax_code']}"
                    )
                )
                continue

            jurisdiction = jurisdictions.get(
                item["jurisdiction"]
            )

            regime, was_created = (
                TaxRegime.objects.update_or_create(
                    code=item["code"],
                    defaults={
                        "name": item["name"],
                        "tax_type": item["tax_type"],
                        "application_type": item["application_type"],
                        "tax": tax,
                        "jurisdiction": jurisdiction,
                        "rate": item["rate"],
                        "minimum_base": item["minimum_base"],
                        "is_active": True,
                    },
                )
            )

            if was_created:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {regime.name}"
                    )
                )
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCompleted. "
                f"Created: {created} | "
                f"Updated: {updated}"
            )
        )