# Regla contable del proyecto

## Regla

Toda creación de asientos contables debe hacerse exclusivamente a través de `AccountingService`.

No se debe crear `JournalEntry` ni `JournalEntryLine` directamente desde modelos, vistas, integraciones o servicios legacy.

La única excepción es la propia clase `AccountingService`, que encapsula la lógica de validación, período, idempotencia y creación de líneas.

## Por qué

Esto evita:
- duplicación de asientos
- dos fuentes de verdad contable
- inconsistencias entre ventas, compras y facturas fiscales
- entradas dobles cuando el mismo evento se dispara más de una vez

## Dónde está la regla aplicada

- Servicio central: `accounting/services/accounting_service.py`
- Wrappers de compatibilidad: `accounting/integration.py`
- Funciones legacy: no deben crear asientos directamente, solo delegan a `AccountingService`

## Ejemplo correcto

from accounting.services import AccountingService

AccountingService.post_sale(sale)
AccountingService.post_purchase(purchase)
AccountingService.post_fiscal_invoice(invoice)

## Ejemplo incorrecto

JournalEntry.objects.create(...)
JournalEntryLine.objects.create(...)
