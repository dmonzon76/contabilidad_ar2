import argparse
import os
import pandas as pd
from decimal import Decimal, InvalidOperation
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from company.models import Company
from products.models import Product
from inventory.models import Location, InventoryItem, InventoryMovement, ProductBatch


class Command(BaseCommand):
    help = "Importa inventario de medicamentos desde un archivo CSV o Excel para una empresa específica en el ERP."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Ruta al archivo CSV o Excel (.xlsx, .xls) con los datos de inventario.",
        )
        parser.add_argument(
            "--company-id",
            type=int,
            required=True,
            help="ID numérico de la empresa (Company) a la cual se asignará el inventario.",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        company_id = options["company_id"]

        if not os.path.exists(file_path):
            raise CommandError(f"El archivo '{file_path}' no existe.")

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise CommandError(f"La empresa con ID {company_id} no fue encontrada en la base de datos.")

        self.stdout.write(
            self.style.NOTICE(f"Iniciando importación para la empresa: '{company.name}' (ID: {company.id})...")
        )

        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext in [".xls", ".xlsx"]:
                df = pd.read_excel(file_path)
            elif ext in [".csv"]:
                df = pd.read_csv(file_path)
            else:
                raise CommandError("Formato de archivo no soportado. Proporcione un archivo .csv, .xls o .xlsx.")
        except Exception as e:
            raise CommandError(f"Error al leer el archivo: {e}")

        # Limpiar encabezados de columnas de espacios adicionales
        df.columns = [str(col).strip() for col in df.columns]

        success_count = 0
        error_count = 0

        for index, row in df.iterrows():
            row_num = index + 2
            try:
                with transaction.atomic():
                    self._process_row(company, row)
                    success_count += 1
            except Exception as e:
                error_count += 1
                self.stderr.write(
                    self.style.ERROR(f"Error en fila {row_num}: {e}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nProceso finalizado:\n"
                f" - Registros procesados exitosamente: {success_count}\n"
                f" - Filas con error: {error_count}"
            )
        )

    def _process_row(self, company, row):
        # 1. Obtener SKU de forma flexible
        sku = self._get_flex_val(row, ["ID Producto (SKU)", "SKU", "ID Producto", "Codigo", "Código"])
        if not sku:
            raise ValueError("El SKU del producto es obligatorio.")

        # 2. Obtener Nombre del Producto de forma flexible
        product_name = self._get_flex_val(row, ["Nombre Medicamento", "Nombre", "Producto", "Medicamento", "Descripción", "Descripcion"])
        if not product_name:
            product_name = f"Producto {sku}"

        # Detectar campos reales del modelo Product en la BD de Django
        product_field_names = [f.name for f in Product._meta.get_fields()]

        # Determinar el nombre del campo para el nombre en el modelo Product (name, nombre, title, etc.)
        name_field = None
        for candidate in ["name", "nombre", "title", "description"]:
            if candidate in product_field_names:
                name_field = candidate
                break

        defaults = {}
        if name_field:
            defaults[name_field] = product_name

        # Manejar atributos en formato JSON si existe el campo 'attributes'
        if "attributes" in product_field_names:
            attributes = {
                "categoria": self._clean_str(self._get_flex_val(row, ["Categoría / Acción", "Categoria", "Categoría"])),
                "laboratorio": self._clean_str(self._get_flex_val(row, ["Laboratorio"])),
                "distribuidora": self._clean_str(self._get_flex_val(row, ["Distribuidora"])),
                "presentacion": self._clean_str(self._get_flex_val(row, ["Tipo Presentación", "Presentación", "Presentacion"])),
                "concentracion": self._clean_str(self._get_flex_val(row, ["Tamaño / Concentración", "Concentración", "Concentracion"])),
                "envase": self._clean_str(self._get_flex_val(row, ["Cantidad por Envase", "Envase"])),
            }
            defaults["attributes"] = {k: v for k, v in attributes.items() if v is not None}

        # 3. Crear o recuperar el Producto
        product, created = Product.objects.get_or_create(
            company=company,
            sku=sku,
            defaults=defaults,
        )

        # Si el producto YA EXISTÍA en la base de datos (por ejemplo de una ejecución previa),
        # get_or_create no aplica defaults, por lo que actualizamos el nombre si estaba vacío.
        updated_fields = []
        if name_field:
            current_name = getattr(product, name_field, None)
            if not current_name or current_name == f"Producto {sku}":
                setattr(product, name_field, product_name)
                updated_fields.append(name_field)

        if "attributes" in product_field_names and defaults.get("attributes"):
            current_attrs = getattr(product, "attributes", None)
            if not current_attrs:
                setattr(product, "attributes", defaults["attributes"])
                updated_fields.append("attributes")

        if updated_fields:
            product.save(update_fields=updated_fields)

        # 4. Ubicación de almacenamiento
        loc_name = self._get_flex_val(row, ["Ubicación Almacén", "Ubicación", "Ubicacion", "Almacén", "Almacen"]) or "Almacén Principal"
        loc_code = loc_name.replace(" ", "-").upper()[:20]

        location, _ = Location.objects.get_or_create(
            company=company,
            name=loc_name,
            defaults={"code": loc_code},
        )

        # 5. Lote y Fecha de Vencimiento
        batch = None
        batch_number = self._get_flex_val(row, ["Número de Lote", "Lote", "Batch"])
        if batch_number:
            exp_date_raw = row.get("Fecha Vencimiento") or row.get("Vencimiento") or row.get("Expiration Date")
            exp_date = self._parse_date(exp_date_raw)

            batch, _ = ProductBatch.objects.get_or_create(
                company=company,
                product=product,
                batch_number=batch_number,
                defaults={"expiration_date": exp_date},
            )

        # 6. InventoryItem (Registro de stock por ubicación)
        item, _ = InventoryItem.objects.get_or_create(
            company=company,
            product=product,
            location=location,
            defaults={"quantity": Decimal("0.00"), "min_stock": Decimal("0.00")},
        )

        # 7. Crear el movimiento de entrada (Stock In)
        qty_raw = row.get("Cantidad Stock") or row.get("Cantidad") or row.get("Stock") or 0
        cost_raw = row.get("Precio Unitario (USD)") or row.get("Precio Unitario") or row.get("Costo Unitario") or row.get("Precio") or 0

        quantity = self._parse_decimal(qty_raw)
        unit_cost = self._parse_decimal(cost_raw)

        if quantity <= 0:
            return

        movement = InventoryMovement(
            company=company,
            item=item,
            batch=batch,
            movement_type="IN",
            quantity=quantity,
            unit_cost=unit_cost,
            note=f"Importación masiva inicial (Lote: {batch_number or 'Sin Lote'})",
        )
        movement.save()

    def _get_flex_val(self, row, possible_keys):
        for key in possible_keys:
            if key in row and pd.notna(row[key]):
                val = str(row[key]).strip()
                if val and val.lower() != "nan":
                    return val
        return None

    def _clean_str(self, val):
        if pd.isna(val) or val is None:
            return None
        s = str(val).strip()
        return s if s and s.lower() != "nan" else None

    def _parse_decimal(self, val):
        if pd.isna(val) or val is None:
            return Decimal("0.00")
        val_str = str(val).replace(",", ".").strip()
        try:
            return Decimal(val_str)
        except (InvalidOperation, ValueError):
            return Decimal("0.00")

    def _parse_date(self, val):
        if pd.isna(val) or val is None:
            return None
        if isinstance(val, (pd.Timestamp, datetime)):
            return val.date()
        val_str = str(val).strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(val_str, fmt).date()
            except ValueError:
                pass
        return None
