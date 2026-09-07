from django.db import migrations


def seed_default_taxes(apps, schema_editor):
    Tax = apps.get_model("fiscal", "Tax")

    taxes = [
        {
            "code": "IVA_10_5",
            "name": "IVA 10.5%",
            "rate": "10.50",
            "is_vat": True,
            "afip_code": 4,
        },
        {
            "code": "IVA_21",
            "name": "IVA 21%",
            "rate": "21.00",
            "is_vat": True,
            "afip_code": 5,
        },
        {
            "code": "IVA_27",
            "name": "IVA 27%",
            "rate": "27.00",
            "is_vat": True,
            "afip_code": 6,
        },
        {
            "code": "IVA_EXENTO",
            "name": "IVA Exento",
            "rate": "0.00",
            "is_exempt": True,
            "afip_code": 3,
        },
        {
            "code": "IVA_NO_GRAVADO",
            "name": "IVA No Gravado",
            "rate": "0.00",
            "is_non_taxed": True,
            "afip_code": 2,
        },
    ]

    for values in taxes:
        code = values.pop("code")
        Tax.objects.update_or_create(code=code, defaults=values)


class Migration(migrations.Migration):
    dependencies = [
        ("fiscal", "0007_remove_fiscalinvoice_customer_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_default_taxes, migrations.RunPython.noop),
    ]
