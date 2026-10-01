from django.db import migrations, models


EXISTING_SUPPLIER_TAX_ID = "30678774495"


def populate_existing_supplier_tax_id(apps, schema_editor):
    Supplier = apps.get_model("suppliers", "Supplier")
    suppliers = Supplier.objects.using(schema_editor.connection.alias)
    missing_tax_id = suppliers.filter(tax_id__isnull=True)

    if not missing_tax_id.exists():
        return

    if suppliers.count() != 1:
        raise RuntimeError(
            "Cannot require supplier CUIT automatically because this database "
            "contains multiple suppliers without a CUIT. Fill their tax_id "
            "values, then rerun this migration."
        )

    missing_tax_id.update(tax_id=EXISTING_SUPPLIER_TAX_ID)


class Migration(migrations.Migration):
    dependencies = [
        ("suppliers", "0005_supplier_tax_id_nullable"),
    ]

    operations = [
        migrations.RunPython(
            populate_existing_supplier_tax_id,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="supplier",
            name="tax_id",
            field=models.CharField(
                max_length=20,
                unique=True,
                verbose_name="CUIT",
            ),
        ),
    ]
