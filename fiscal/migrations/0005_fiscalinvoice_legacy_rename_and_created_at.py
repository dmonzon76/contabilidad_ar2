import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fiscal", "0004_tax_alter_electronicvoucherbook_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="fiscalinvoice",
            old_name="exempt_amount",
            new_name="net_amount",
        ),
        migrations.RenameField(
            model_name="fiscalinvoice",
            old_name="voucher_number",
            new_name="number",
        ),
        migrations.RenameField(
            model_name="fiscalinvoice",
            old_name="non_taxed_amount",
            new_name="perception_amount",
        ),
        migrations.RenameField(
            model_name="fiscalinvoice",
            old_name="subtotal",
            new_name="retention_amount",
        ),
        migrations.RenameField(
            model_name="fiscalinvoice",
            old_name="total",
            new_name="tax_amount",
        ),
        migrations.RenameField(
            model_name="fiscalinvoice",
            old_name="vat_amount",
            new_name="total_amount",
        ),
        migrations.AddField(
            model_name="fiscalinvoice",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
    ]
