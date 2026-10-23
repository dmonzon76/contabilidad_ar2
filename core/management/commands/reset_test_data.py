from django.core.management.base import BaseCommand
from django.db import transaction

from accounting.models import (
    JournalEntry,
    JournalEntryLine,
)
from accounting.models.account_movement import AccountMovement
from inventory.models import (
    InventoryMovement,
)
from purchases.models import (
    Purchase,
    PurchaseLine,
    PurchasePerception,
    PurchaseRetention,
    PurchaseTax,
)
from sales.models import (
    Sale,
    SaleItem,
)


class Command(BaseCommand):
    help = "Delete all transactional test data"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write("=== RESET TEST DATA ===")

        # Accounting
        JournalEntryLine.objects.all().delete()
        JournalEntry.objects.all().delete()
        AccountMovement.objects.all().delete()

        # Inventory
        InventoryMovement.objects.all().delete()

        # Purchases
        PurchaseTax.objects.all().delete()
        PurchasePerception.objects.all().delete()
        PurchaseRetention.objects.all().delete()
        PurchaseLine.objects.all().delete()
        Purchase.objects.all().delete()

        # Sales
        SaleItem.objects.all().delete()
        Sale.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Transactional data deleted successfully."
            )
        )