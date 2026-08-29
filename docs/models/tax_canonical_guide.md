# Guía del modelo Tax como fuente canónica

## Regla principal
El modelo `Tax` es la fuente única de verdad para tasas e impuestos fiscales del sistema.

## Modelos que deben usar Tax
- `products.Product.tax`
- `sales.models.sale_item.SaleItem.tax`
- `inventory.models.InventoryMovement.internal_tax`
- `purchases.models.purchase.PurchaseTax.tax`
- `fiscal.models.fiscal_invoice_line.FiscalInvoiceLine.tax`
- `fiscal.models.fiscal_product.FiscalProduct.tax`
- `fiscal.models.fiscal_service.FiscalService.tax`

## Reglas de uso
- No usar `vat_type`, `tax_category`, ni valores hardcodeados como `21` o `GRAVADO` para lógica fiscal.
- Para calcular IVA o impuestos, usar `Tax.rate` y el atributo booleano correspondiente (`is_vat`, `is_exempt`, `is_non_taxed`, etc.).
- Los campos legados deben mantenerse solo como compatibilidad temporal y deben migrarse a `Tax`.

## Ejemplo de cálculo
```python
if item.tax and item.tax.is_vat:
    iva = item.subtotal * (item.tax.rate / Decimal("100"))
```

## Recomendación de mantenimiento
- Evitar nuevos campos tipo de impuesto customizados fuera de `Tax`.
- Cuando se agregue un nuevo tipo fiscal, debe reflejarse primero en `fiscal.models.tax.Tax`.
- Mantener migraciones pequeñas y comprobables.
