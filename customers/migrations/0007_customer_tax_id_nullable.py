from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0006_alter_customer_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="tax_id",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                verbose_name="CUIT",
            ),
        ),
    ]
