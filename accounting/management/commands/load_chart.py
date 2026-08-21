from django.core.management.base import BaseCommand
from accounting.models import Account
from company.models import Company

# PLAN PROFESIONAL COMPLETO (solo estructura, te lo genero abajo)
PLAN = [
    # code, name, account_type, parent_code
    ("1", "Activo", "ASSET", None),
    ("1.1", "Activo Corriente", "ASSET", "1"),
    ("1.1.01", "Caja", "ASSET", "1.1"),
    ("1.1.02", "Bancos", "ASSET", "1.1"),
    ("1.1.03", "Valores a Depositar", "ASSET", "1.1"),
    ("1.1.04", "Cuentas por Cobrar", "ASSET", "1.1"),
    ("1.1.05", "Deudores Varios", "ASSET", "1.1"),
    ("1.1.06", "Anticipos a Proveedores", "ASSET", "1.1"),
    ("1.1.07", "Crédito Fiscal IVA", "ASSET", "1.1"),
    ("1.1.08", "Crédito Fiscal IIBB", "ASSET", "1.1"),
    ("1.1.09", "Inventario Mercaderías", "ASSET", "1.1"),
    ("1.1.10", "Inventario Insumos", "ASSET", "1.1"),
    ("1.1.11", "Inventario Productos Terminados", "ASSET", "1.1"),

    ("1.2", "Activo No Corriente", "ASSET", "1"),
    ("1.2.01", "Bienes de Uso - Muebles", "ASSET", "1.2"),
    ("1.2.02", "Bienes de Uso - Equipos", "ASSET", "1.2"),
    ("1.2.03", "Bienes de Uso - Rodados", "ASSET", "1.2"),
    ("1.2.04", "Bienes de Uso - Inmuebles", "ASSET", "1.2"),
    ("1.2.05", "Amortización Acumulada - Muebles", "ASSET", "1.2"),
    ("1.2.06", "Amortización Acumulada - Equipos", "ASSET", "1.2"),
    ("1.2.07", "Amortización Acumulada - Rodados", "ASSET", "1.2"),
    ("1.2.08", "Amortización Acumulada - Inmuebles", "ASSET", "1.2"),

    ("2", "Pasivo", "LIABILITY", None),
    ("2.1", "Pasivo Corriente", "LIABILITY", "2"),
    ("2.1.01", "Proveedores", "LIABILITY", "2.1"),
    ("2.1.02", "Proveedores Extranjeros", "LIABILITY", "2.1"),
    ("2.1.03", "Sueldos a Pagar", "LIABILITY", "2.1"),
    ("2.1.04", "Cargas Sociales a Pagar", "LIABILITY", "2.1"),
    ("2.1.05", "IVA Débito Fiscal", "LIABILITY", "2.1"),
    ("2.1.06", "IIBB a Pagar", "LIABILITY", "2.1"),
    ("2.1.07", "Ganancias a Pagar", "LIABILITY", "2.1"),
    ("2.1.08", "Retenciones a Pagar", "LIABILITY", "2.1"),
    ("2.1.09", "Anticipos de Clientes", "LIABILITY", "2.1"),
    ("2.1.10", "Deudas Bancarias CP", "LIABILITY", "2.1"),

    ("2.2", "Pasivo No Corriente", "LIABILITY", "2"),
    ("2.2.01", "Préstamos LP", "LIABILITY", "2.2"),
    ("2.2.02", "Deudas Financieras LP", "LIABILITY", "2.2"),

    ("3", "Patrimonio Neto", "EQUITY", None),
    ("3.1", "Capital Social", "EQUITY", "3"),
    ("3.2", "Ajuste de Capital", "EQUITY", "3"),
    ("3.3", "Reservas", "EQUITY", "3"),
    ("3.4", "Resultados Acumulados", "EQUITY", "3"),
    ("3.5", "Resultado del Ejercicio", "EQUITY", "3"),

    ("4", "Ingresos", "INCOME", None),
    ("4.1", "Ventas", "INCOME", "4"),
    ("4.1.01", "Ventas de Productos", "INCOME", "4.1"),
    ("4.1.02", "Ventas de Servicios", "INCOME", "4.1"),
    ("4.1.03", "Ventas Exentas", "INCOME", "4.1"),
    ("4.1.04", "Ventas No Gravadas", "INCOME", "4.1"),
    ("4.1.05", "Ventas CF", "INCOME", "4.1"),
    ("4.1.06", "Ventas RI", "INCOME", "4.1"),
    ("4.1.07", "Ventas Monotributo", "INCOME", "4.1"),
    ("4.1.08", "Ventas Exterior", "INCOME", "4.1"),

    ("4.2", "Otros Ingresos", "INCOME", "4"),
    ("4.2.01", "Intereses Ganados", "INCOME", "4.2"),
    ("4.2.02", "Diferencias de Cambio Positivas", "INCOME", "4.2"),
    ("4.2.03", "Recupero de Gastos", "INCOME", "4.2"),
    ("4.2.04", "Ingresos Extraordinarios", "INCOME", "4.2"),

    ("5", "Costos", "EXPENSE", None),
    ("5.1", "Costos de Productos", "EXPENSE", "5"),
    ("5.1.01", "Costo Mercadería Vendida", "EXPENSE", "5.1"),
    ("5.1.02", "Costo Insumos", "EXPENSE", "5.1"),
    ("5.1.03", "Costo Producción", "EXPENSE", "5.1"),
    ("5.1.04", "Ajuste Inventario", "EXPENSE", "5.1"),

    ("5.2", "Costos de Servicios", "EXPENSE", "5"),
    ("5.2.01", "Costo Servicios Prestados", "EXPENSE", "5.2"),
    ("5.2.02", "Subcontrataciones", "EXPENSE", "5.2"),
    ("5.2.03", "Honorarios Técnicos", "EXPENSE", "5.2"),

    ("6", "Gastos", "EXPENSE", None),
    ("6.1", "Gastos Administrativos", "EXPENSE", "6"),
    ("6.1.01", "Sueldos Administrativos", "EXPENSE", "6.1"),
    ("6.1.02", "Cargas Sociales", "EXPENSE", "6.1"),
    ("6.1.03", "Servicios Públicos", "EXPENSE", "6.1"),
    ("6.1.04", "Alquileres", "EXPENSE", "6.1"),
    ("6.1.05", "Seguros", "EXPENSE", "6.1"),
    ("6.1.06", "Papelería", "EXPENSE", "6.1"),
    ("6.1.07", "Gastos Bancarios", "EXPENSE", "6.1"),
    ("6.1.08", "Honorarios", "EXPENSE", "6.1"),

    ("6.2", "Gastos Comerciales", "EXPENSE", "6"),
    ("6.2.01", "Sueldos Comerciales", "EXPENSE", "6.2"),
    ("6.2.02", "Publicidad", "EXPENSE", "6.2"),
    ("6.2.03", "Comisiones", "EXPENSE", "6.2"),
    ("6.2.04", "Viáticos", "EXPENSE", "6.2"),
    ("6.2.05", "Fletes", "EXPENSE", "6.2"),

    ("6.3", "Gastos Financieros", "EXPENSE", "6"),
    ("6.3.01", "Intereses Pagados", "EXPENSE", "6.3"),
    ("6.3.02", "Diferencias de Cambio Negativas", "EXPENSE", "6.3"),
    ("6.3.03", "Gastos Financieros Varios", "EXPENSE", "6.3"),

    ("7", "Impuestos", "LIABILITY", None),
    ("7.1", "IVA Débito Fiscal", "LIABILITY", "7"),
    ("7.2", "IVA Crédito Fiscal", "LIABILITY", "7"),
    ("7.3", "Ingresos Brutos", "LIABILITY", "7"),
    ("7.4", "Impuesto a las Ganancias", "LIABILITY", "7"),
    ("7.5", "Impuesto al Cheque", "LIABILITY", "7"),
    ("7.6", "Retenciones Sufridas", "LIABILITY", "7"),
    ("7.7", "Retenciones Practicadas", "LIABILITY", "7"),
]


class Command(BaseCommand):
    help = "Load professional chart of accounts for a company"

    def add_arguments(self, parser):
        parser.add_argument("company_id", type=int)

    def handle(self, *args, **kwargs):
        company_id = kwargs["company_id"]
        company = Company.objects.get(id=company_id)

        self.stdout.write(f"Loading chart of accounts for {company.name}")

        for code, name, acc_type, parent_code in PLAN:

            # Si ya existe → no lo toca
            if Account.objects.filter(company=company, code=code).exists():
                continue

            parent = None
            if parent_code:
                parent = Account.objects.filter(company=company, code=parent_code).first()

            Account.objects.create(
                company=company,
                code=code,
                name=name,
                account_type=acc_type,
                parent=parent,
                is_active=True,
            )

        self.stdout.write(self.style.SUCCESS("Professional chart of accounts loaded successfully"))
