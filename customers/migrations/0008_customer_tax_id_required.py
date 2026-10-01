from django.db import migrations, models
from django.db.models import Q


def ensure_existing_customers_have_tax_id(apps, schema_editor):
    Customer = apps.get_model("customers", "Customer")
    missing_tax_id = Customer.objects.using(schema_editor.connection.alias).filter(
        Q(tax_id__isnull=True) | Q(tax_id="")
    )
    if missing_tax_id.exists():
        raise RuntimeError(
            "Cannot require customer CUIT while existing customers have no CUIT. "
            "Fill their tax_id values, then rerun this migration."
        )


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0007_customer_tax_id_nullable"),
    ]

    operations = [
        migrations.RunPython(
            ensure_existing_customers_have_tax_id,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="customer",
            name="tax_id",
            field=models.CharField(
                max_length=20,
                verbose_name="CUIT",
            ),
        ),
    ]
