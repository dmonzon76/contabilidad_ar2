from django.core.management.base import BaseCommand
from accounting.models import Account
from company.models import Company

PLAN = [
    ("1", "Activo", "ASSET", None),

    ("1.1", "Activo Corriente", "ASSET", "1"),
    ("1.1.1", "Disponibilidades", "ASSET", "1.1"),
    ("1.1.1.01", "Caja", "ASSET", "1.1.1"),
    ("1.1.1.02", "Bancos", "ASSET", "1.1.1"),
    ("1.1.1.03", "Valores a Depositar", "ASSET", "1.1.1"),

    ("1.1.2", "Créditos por Ventas", "ASSET", "1.1"),
    ("1.1.3", "Otros Créditos", "ASSET", "1.1"),

    ("1.2", "Activo No Corriente", "ASSET", "1"),
    ("1.2.1", "Inversiones", "ASSET", "1.2"),
    ("1.2.2", "Bienes de Uso", "ASSET", "1.2"),
    ("1.2.3", "Activos Intangibles", "ASSET", "1.2"),

    ("2", "Pasivo", "LIABILITY", None),
    ("2.1", "Pasivo Corriente", "LIABILITY", "2"),
    ("2.2", "Pasivo No Corriente", "LIABILITY", "2"),

    ("3", "Patrimonio Neto", "EQUITY", None),

    ("4", "Ingresos", "INCOME", None),
    ("4.1", "Ventas", "INCOME", "4"),

    ("5", "Gastos", "EXPENSE", None),
    ("5.1", "Compras", "EXPENSE", "5"),
    ("5.2", "Sueldos", "EXPENSE", "5"),
    ("5.3", "Servicios", "EXPENSE", "5"),
]


class Command(BaseCommand):
    help = "Load professional chart of accounts for a company"

    def add_arguments(self, parser):
        parser.add_argument("company_id", type=int)

    def handle(self, *args, **kwargs):
        company_id = kwargs["company_id"]
        company = Company.objects.get(id=company_id)

        self.stdout.write(f"Loading chart of accounts for {company.name}")

        accounts = {}

        for code, name, acc_type, parent_code in PLAN:
            parent = accounts.get(parent_code)

            acc = Account.objects.create(
                company=company,
                code=code,
                name=name,
                account_type=acc_type,
                parent=parent,
            )

            accounts[code] = acc

        self.stdout.write(self.style.SUCCESS("Professional chart of accounts loaded successfully"))
