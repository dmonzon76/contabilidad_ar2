from django.db import migrations, models
class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0007_alter_account_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="journalentry",
            name="source_key",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                unique=True,
            ),
        ),
        migrations.AddConstraint(
            model_name="journalentry",
            constraint=models.UniqueConstraint(
                fields=("company", "purchase"),
                name="unique_purchase_journal_entry",
            ),
        ),
    ]
