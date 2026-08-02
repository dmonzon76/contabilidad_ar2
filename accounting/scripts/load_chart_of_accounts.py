from accounting.models import Account
from company.models import Company

PLAN_DE_CUENTAS = [

    # -------------------------
    # 1 - ACTIVO
    # -------------------------
    {"code": "1", "name": "Activo", "type": "ASSET", "parent": None},
    {"code": "1.1", "name": "Activo Corriente", "type": "ASSET", "parent": "1"},

    {"code": "1.1.01", "name": "Caja y Bancos", "type": "ASSET", "parent": "1.1"},
    {"code": "1.1.01.001", "name": "Caja", "type": "ASSET", "parent": "1.1.01"},
    {"code": "1.1.01.002", "name": "Banco Nación Cta Cte", "type": "ASSET", "parent": "1.1.01"},
    {"code": "1.1.01.003", "name": "Banco Provincia Cta Cte", "type": "ASSET", "parent": "1.1.01"},
    {"code": "1.1.01.004", "name": "Banco Santander Cta Cte", "type": "ASSET", "parent": "1.1.01"},
    {"code": "1.1.01.005", "name": "Valores a Depositar", "type": "ASSET", "parent": "1.1.01"},

    {"code": "1.1.02", "name": "Créditos por Ventas", "type": "ASSET", "parent": "1.1"},
    {"code": "1.1.02.001", "name": "Clientes", "type": "ASSET", "parent": "1.1.02"},
    {"code": "1.1.02.002", "name": "Clientes del Exterior", "type": "ASSET", "parent": "1.1.02"},
    {"code": "1.1.02.003", "name": "Documentos a Cobrar", "type": "ASSET", "parent": "1.1.02"},
    {"code": "1.1.02.004", "name": "Previsión Incobrables", "type": "ASSET", "parent": "1.1.02"},

    {"code": "1.1.03", "name": "Otros Créditos", "type": "ASSET", "parent": "1.1"},
    {"code": "1.1.03.001", "name": "Anticipos a Proveedores", "type": "ASSET", "parent": "1.1.03"},
    {"code": "1.1.03.002", "name": "Crédito Fiscal IVA", "type": "ASSET", "parent": "1.1.03"},
    {"code": "1.1.03.003", "name": "Saldo a favor AFIP", "type": "ASSET", "parent": "1.1.03"},
    {"code": "1.1.03.004", "name": "Saldo a favor ARBA / AGIP", "type": "ASSET", "parent": "1.1.03"},
    {"code": "1.1.03.005", "name": "Préstamos Otorgados", "type": "ASSET", "parent": "1.1.03"},

    {"code": "1.1.04", "name": "Bienes de Cambio", "type": "ASSET", "parent": "1.1"},
    {"code": "1.1.04.001", "name": "Mercaderías", "type": "ASSET", "parent": "1.1.04"},
    {"code": "1.1.04.002", "name": "Productos Terminados", "type": "ASSET", "parent": "1.1.04"},
    {"code": "1.1.04.003", "name": "Materias Primas", "type": "ASSET", "parent": "1.1.04"},
    {"code": "1.1.04.004", "name": "Envases y Embalajes", "type": "ASSET", "parent": "1.1.04"},

    {"code": "1.2", "name": "Activo No Corriente", "type": "ASSET", "parent": "1"},

    {"code": "1.2.01", "name": "Bienes de Uso", "type": "ASSET", "parent": "1.2"},
    {"code": "1.2.01.001", "name": "Terrenos", "type": "ASSET", "parent": "1.2.01"},
    {"code": "1.2.01.002", "name": "Edificios", "type": "ASSET", "parent": "1.2.01"},
    {"code": "1.2.01.003", "name": "Muebles y Útiles", "type": "ASSET", "parent": "1.2.01"},
    {"code": "1.2.01.004", "name": "Rodados", "type": "ASSET", "parent": "1.2.01"},
    {"code": "1.2.01.005", "name": "Equipos de Computación", "type": "ASSET", "parent": "1.2.01"},
    {"code": "1.2.01.006", "name": "Maquinarias", "type": "ASSET", "parent": "1.2.01"},
    {"code": "1.2.01.007", "name": "Herramientas", "type": "ASSET", "parent": "1.2.01"},
    {"code": "1.2.01.900", "name": "Amortización Acumulada", "type": "ASSET", "parent": "1.2.01"},

    {"code": "1.2.02", "name": "Activos Intangibles", "type": "ASSET", "parent": "1.2"},
    {"code": "1.2.02.001", "name": "Marcas y Patentes", "type": "ASSET", "parent": "1.2.02"},
    {"code": "1.2.02.002", "name": "Software", "type": "ASSET", "parent": "1.2.02"},
    {"code": "1.2.02.900", "name": "Amortización Acumulada", "type": "ASSET", "parent": "1.2.02"},

    {"code": "1.2.03", "name": "Inversiones", "type": "ASSET", "parent": "1.2"},
    {"code": "1.2.03.001", "name": "Inversiones a Largo Plazo", "type": "ASSET", "parent": "1.2.03"},
    {"code": "1.2.03.002", "name": "Títulos Públicos", "type": "ASSET", "parent": "1.2.03"},
    {"code": "1.2.03.003", "name": "Plazos Fijos", "type": "ASSET", "parent": "1.2.03"},

    # -------------------------
    # 2 - PASIVO
    # -------------------------
    {"code": "2", "name": "Pasivo", "type": "LIABILITY", "parent": None},
    {"code": "2.1", "name": "Pasivo Corriente", "type": "LIABILITY", "parent": "2"},

    {"code": "2.1.01", "name": "Deudas Comerciales", "type": "LIABILITY", "parent": "2.1"},
    {"code": "2.1.01.001", "name": "Proveedores", "type": "LIABILITY", "parent": "2.1.01"},
    {"code": "2.1.01.002", "name": "Proveedores del Exterior", "type": "LIABILITY", "parent": "2.1.01"},
    {"code": "2.1.01.003", "name": "Documentos a Pagar", "type": "LIABILITY", "parent": "2.1.01"},

    {"code": "2.1.02", "name": "Deudas Fiscales", "type": "LIABILITY", "parent": "2.1"},
    {"code": "2.1.02.001", "name": "IVA Débito Fiscal", "type": "LIABILITY", "parent": "2.1.02"},
    {"code": "2.1.02.002", "name": "Retenciones AFIP", "type": "LIABILITY", "parent": "2.1.02"},
    {"code": "2.1.02.003", "name": "Retenciones ARBA / AGIP", "type": "LIABILITY", "parent": "2.1.02"},
    {"code": "2.1.02.004", "name": "Ingresos Brutos", "type": "LIABILITY", "parent": "2.1.02"},
    {"code": "2.1.02.005", "name": "Impuesto a las Ganancias", "type": "LIABILITY", "parent": "2.1.02"},

    {"code": "2.1.03", "name": "Deudas Sociales", "type": "LIABILITY", "parent": "2.1"},
    {"code": "2.1.03.001", "name": "Sueldos a Pagar", "type": "LIABILITY", "parent": "2.1.03"},
    {"code": "2.1.03.002", "name": "Cargas Sociales", "type": "LIABILITY", "parent": "2.1.03"},
    {"code": "2.1.03.003", "name": "ART / Seguros", "type": "LIABILITY", "parent": "2.1.03"},

    {"code": "2.1.04", "name": "Préstamos", "type": "LIABILITY", "parent": "2.1"},
    {"code": "2.1.04.001", "name": "Préstamos Bancarios CP", "type": "LIABILITY", "parent": "2.1.04"},
    {"code": "2.1.04.002", "name": "Descubiertos Bancarios", "type": "LIABILITY", "parent": "2.1.04"},

    {"code": "2.2", "name": "Pasivo No Corriente", "type": "LIABILITY", "parent": "2"},

    {"code": "2.2.01", "name": "Préstamos LP", "type": "LIABILITY", "parent": "2.2"},
    {"code": "2.2.01.001", "name": "Préstamos Bancarios LP", "type": "LIABILITY", "parent": "2.2.01"},
    {"code": "2.2.01.002", "name": "Obligaciones Negociables", "type": "LIABILITY", "parent": "2.2.01"},

    {"code": "2.2.02", "name": "Provisiones", "type": "LIABILITY", "parent": "2.2"},
    {"code": "2.2.02.001", "name": "Provisión para Juicios", "type": "LIABILITY", "parent": "2.2.02"},
    {"code": "2.2.02.002", "name": "Provisión para Garantías", "type": "LIABILITY", "parent": "2.2.02"},

    # -------------------------
    # 3 - PATRIMONIO NETO
    # -------------------------
    {"code": "3", "name": "Patrimonio Neto", "type": "EQUITY", "parent": None},

    {"code": "3.1", "name": "Capital", "type": "EQUITY", "parent": "3"},
    {"code": "3.1.01", "name": "Capital Social", "type": "EQUITY", "parent": "3.1"},
    {"code": "3.1.02", "name": "Ajuste de Capital", "type": "EQUITY", "parent": "3.1"},

    {"code": "3.2", "name": "Resultados", "type": "EQUITY", "parent": "3"},
    {"code": "3.2.01", "name": "Resultados Acumulados", "type": "EQUITY", "parent": "3.2"},
    {"code": "3.2.02", "name": "Resultado del Ejercicio", "type": "EQUITY", "parent": "3.2"},

    {"code": "3.3", "name": "Aportes", "type": "EQUITY", "parent": "3"},
    {"code": "3.3.01", "name": "Aportes Irrevocables", "type": "EQUITY", "parent": "3.3"},
    {"code": "3.3.02", "name": "Reservas Legales", "type": "EQUITY", "parent": "3.3"},
    {"code": "3.3.03", "name": "Reservas Facultativas", "type": "EQUITY", "parent": "3.3"},

    # -------------------------
    # 4 - INGRESOS
    # -------------------------
    {"code": "4", "name": "Ingresos", "type": "INCOME", "parent": None},

    {"code": "4.1", "name": "Ingresos por Ventas", "type": "INCOME", "parent": "4"},
    {"code": "4.1.01", "name": "Ventas de Mercaderías", "type": "INCOME", "parent": "4.1"},
    {"code": "4.1.02", "name": "Ventas de Servicios", "type": "INCOME", "parent": "4.1"},
    {"code": "4.1.03", "name": "Ventas del Exterior", "type": "INCOME", "parent": "4.1"},

    {"code": "4.2", "name": "Otros Ingresos", "type": "INCOME", "parent": "4"},
    {"code": "4.2.01", "name": "Intereses Ganados", "type": "INCOME", "parent": "4.2"},
    {"code": "4.2.02", "name": "Diferencias de Cambio Positivas", "type": "INCOME", "parent": "4.2"},
    {"code": "4.2.03", "name": "Recupero de Gastos", "type": "INCOME", "parent": "4.2"},

    # -------------------------
    # 5 - COSTOS
    # -------------------------
    {"code": "5", "name": "Costos", "type": "EXPENSE", "parent": None},

    {"code": "5.1", "name": "Costos de Mercaderías Vendidas", "type": "EXPENSE", "parent": "5"},
    {"code": "5.1.01", "name": "CMV Mercaderías", "type": "EXPENSE", "parent": "5.1"},
    {"code": "5.1.02", "name": "CMV Producción", "type": "EXPENSE", "parent": "5.1"},

    {"code": "5.2", "name": "Costos de Servicios", "type": "EXPENSE", "parent": "5"},
    {"code": "5.2.01", "name": "Costos Operativos", "type": "EXPENSE", "parent": "5.2"},

    # -------------------------
    # 6 - GASTOS
    # -------------------------
    {"code": "6", "name": "Gastos", "type": "EXPENSE", "parent": None},

    {"code": "6.1", "name": "Gastos de Administración", "type": "EXPENSE", "parent": "6"},
    {"code": "6.1.01", "name": "Sueldos y Jornales", "type": "EXPENSE", "parent": "6.1"},
    {"code": "6.1.02", "name": "Honorarios", "type": "EXPENSE", "parent": "6.1"},
    {"code": "6.1.03", "name": "Servicios Públicos", "type": "EXPENSE", "parent": "6.1"},
    {"code": "6.1.04", "name": "Alquileres", "type": "EXPENSE", "parent": "6.1"},
    {"code": "6.1.05", "name": "Seguros", "type": "EXPENSE", "parent": "6.1"},
    {"code": "6.1.06", "name": "Gastos de Oficina", "type": "EXPENSE", "parent": "6.1"},

    {"code": "6.2", "name": "Gastos de Ventas", "type": "EXPENSE", "parent": "6"},
    {"code": "6.2.01", "name": "Publicidad", "type": "EXPENSE", "parent": "6.2"},
    {"code": "6.2.02", "name": "Comisiones", "type": "EXPENSE
