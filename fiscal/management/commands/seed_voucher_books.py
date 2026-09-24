from django.core.management.base import BaseCommand
from company.models import Company
from fiscal.models import ElectronicVoucherBook


class Command(BaseCommand):
    help = "Inicializa los talonarios electrónicos (FA, FB, FC) para el Punto de Venta 1 de las empresas."

    def add_arguments(self, parser):
        parser.add_argument(
            "--company_id",
            type=int,
            help="ID opcional de la empresa específica para la cual dar de alta los talonarios.",
        )

    def handle(self, *args, **options):
        company_id = options.get("company_id")

        if company_id:
            companies = Company.objects.filter(pk=company_id)
            if not companies.exists():
                self.stderr.write(
                    self.style.ERROR(f"No se encontró ninguna empresa con ID {company_id}.")
                )
                return
        else:
            companies = Company.objects.all()

        if not companies.exists():
            self.stderr.write(
                self.style.WARNING("No existen empresas registradas en la base de datos.")
            )
            return

        # Tipos de comprobantes principales para facturación electrónica
        voucher_types = [
            ("FA", "Factura A"),
            ("FB", "Factura B"),
            ("FC", "Factura C"),
        ]

        point_of_sale = 1  # Punto de Venta activo por defecto

        for company in companies:
            self.stdout.write(f"\nProcesando empresa: {company.name} (ID: {company.id})...")
            created_count = 0

            for v_type, v_name in voucher_types:
                vb, created = ElectronicVoucherBook.objects.get_or_create(
                    company=company,
                    point_of_sale=point_of_sale,
                    voucher_type=v_type,
                    defaults={
                        "current_number": 0,
                        "enabled": True,
                    },
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  + Creado talonario {v_type} ({v_name}) para PV {point_of_sale}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"  . El talonario {v_type} ({v_name}) para PV {point_of_sale} ya existía"
                        )
                    )

            if created_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f"Se crearon {created_count} nuevos talonarios para {company.name}.")
                )

        self.stdout.write(self.style.SUCCESS("\n¡Inicialización de talonarios completada con éxito!"))