from django.core.management.base import BaseCommand

from fiscal.models.tax_jurisdiction import TaxJurisdiction


class Command(BaseCommand):

    help = "Carga las jurisdicciones fiscales maestras"

    JURISDICTIONS = [

        # Organismos nacionales

        {
            "code": "AFIP",
            "name": "AFIP",
            "is_national": True,
        },

        {
            "code": "SIRCREB",
            "name": "SIRCREB",
            "is_national": True,
        },

        # CABA

        {
            "code": "AGIP",
            "name": "CABA (AGIP)",
            "is_provincial": True,
        },

        # Buenos Aires

        {
            "code": "ARBA",
            "name": "Buenos Aires (ARBA)",
            "is_provincial": True,
        },

        # Provincias

        {
            "code": "CORDOBA",
            "name": "Córdoba",
            "is_provincial": True,
        },

        {
            "code": "SANTA_FE",
            "name": "Santa Fe",
            "is_provincial": True,
        },

        {
            "code": "MENDOZA",
            "name": "Mendoza",
            "is_provincial": True,
        },

        {
            "code": "TUCUMAN",
            "name": "Tucumán",
            "is_provincial": True,
        },

        {
            "code": "SALTA",
            "name": "Salta",
            "is_provincial": True,
        },

        {
            "code": "CHACO",
            "name": "Chaco",
            "is_provincial": True,
        },

        {
            "code": "MISIONES",
            "name": "Misiones",
            "is_provincial": True,
        },

        {
            "code": "ENTRE_RIOS",
            "name": "Entre Ríos",
            "is_provincial": True,
        },

        {
            "code": "NEUQUEN",
            "name": "Neuquén",
            "is_provincial": True,
        },

        {
            "code": "SAN_JUAN",
            "name": "San Juan",
            "is_provincial": True,
        },

        {
            "code": "SAN_LUIS",
            "name": "San Luis",
            "is_provincial": True,
        },

        {
            "code": "LA_PAMPA",
            "name": "La Pampa",
            "is_provincial": True,
        },

        {
            "code": "RIO_NEGRO",
            "name": "Río Negro",
            "is_provincial": True,
        },

        {
            "code": "CHUBUT",
            "name": "Chubut",
            "is_provincial": True,
        },

        {
            "code": "SANTA_CRUZ",
            "name": "Santa Cruz",
            "is_provincial": True,
        },

        {
            "code": "TIERRA_DEL_FUEGO",
            "name": "Tierra del Fuego",
            "is_provincial": True,
        },

        {
            "code": "CATAMARCA",
            "name": "Catamarca",
            "is_provincial": True,
        },

        {
            "code": "LA_RIOJA",
            "name": "La Rioja",
            "is_provincial": True,
        },

        {
            "code": "JUJUY",
            "name": "Jujuy",
            "is_provincial": True,
        },

        {
            "code": "FORMOSA",
            "name": "Formosa",
            "is_provincial": True,
        },

        {
            "code": "SANTIAGO_DEL_ESTERO",
            "name": "Santiago del Estero",
            "is_provincial": True,
        },

        {
            "code": "CORRIENTES",
            "name": "Corrientes",
            "is_provincial": True,
        },

        {
            "code": "MULTIJURISDICCIONAL",
            "name": "Convenio Multilateral",
            "is_national": True,
        },
    ]

    def handle(self, *args, **options):

        created = 0
        updated = 0

        for item in self.JURISDICTIONS:

            jurisdiction, was_created = (
                TaxJurisdiction.objects.update_or_create(
                    code=item["code"],
                    defaults={
                        "name": item["name"],
                        "is_national": item.get(
                            "is_national",
                            False,
                        ),
                        "is_provincial": item.get(
                            "is_provincial",
                            False,
                        ),
                        "is_municipal": item.get(
                            "is_municipal",
                            False,
                        ),
                        "is_active": True,
                    },
                )
            )

            if was_created:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {jurisdiction.name}"
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