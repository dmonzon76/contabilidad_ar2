from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("suppliers", "0004_alter_supplier_tax_profile_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplier",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="supplier",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name="supplier",
            name="tax_id",
            field=models.CharField(
                max_length=20,
                null=True,
                unique=True,
                verbose_name="CUIT",
            ),
        ),
    ]
