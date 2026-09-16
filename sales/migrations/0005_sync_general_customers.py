from django.db import migrations


def copy_general_customers_to_sales(apps, schema_editor):
    general_customer = apps.get_model("customers", "Customer")
    sales_customer = apps.get_model("sales", "Customer")

    for customer in general_customer.objects.all().iterator():
        sales_customer.objects.update_or_create(
            company_id=customer.company_id,
            name=customer.name,
            defaults={
                "tax_id": customer.tax_id,
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address,
                "is_active": customer.is_active,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0004_customer_ganancias_rate_customer_iibb_rate_and_more"),
        ("sales", "0004_alter_sale_options_alter_saleitem_options_and_more"),
    ]

    operations = [
        migrations.RunPython(
            copy_general_customers_to_sales, migrations.RunPython.noop
        ),
    ]
