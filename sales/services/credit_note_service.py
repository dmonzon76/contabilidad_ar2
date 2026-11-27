from django.db import transaction

import inventory.models
from accounting.models import AccountMovement, JournalEntry
from accounting.services import AccountingService


class CreditNoteService:
    @staticmethod
    def reverse_customer_ledger(
        credit_note,
    ):
        AccountMovement.objects.create(
            company=credit_note.company,
            customer=credit_note.customer,
            movement_type="CREDIT",
            amount=credit_note.total_amount,
            description=f"Credit Note {credit_note.number}",
        )

    @staticmethod
    def reverse_journal_entry(
        credit_note,
    ):
        sale = credit_note.sale

        sale_entry = JournalEntry.objects.filter(source_key=f"sale:{sale.pk}").first()

        if not sale_entry:
            return

        AccountingService.reverse_entry(sale_entry)

    @staticmethod
    def reverse_inventory(
        credit_note,
    ):
        sale = credit_note.sale

        for sale_item in sale.items.all():
            if not sale_item.product or sale_item.product.is_service:
                continue

            inventory_item = inventory.models.InventoryItem.objects.get(
                company=credit_note.company,
                product=sale_item.product,
            )

            inventory.models.InventoryMovement.objects.create(
                company=credit_note.company,
                item=inventory_item,
                movement_type="IN",
                quantity=sale_item.quantity,
                unit_cost=sale_item.unit_cost,
                note=f"Credit Note {credit_note.number}",
            )

    @staticmethod
    @transaction.atomic
    def issue_credit_note(
        credit_note,
    ):

        if credit_note.status == "ISSUED":
            return credit_note

        CreditNoteService.reverse_customer_ledger(credit_note)

        CreditNoteService.reverse_inventory(credit_note)

        CreditNoteService.reverse_journal_entry(credit_note)

        credit_note.status = "ISSUED"

        credit_note.save(
            update_fields=[
                "status",
            ]
        )

        return credit_note
