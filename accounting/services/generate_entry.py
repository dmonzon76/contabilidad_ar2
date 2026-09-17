# accounting/services/generate_entry.py

from accounting.services.accounting_service import AccountingService


def generate_accounting_entry(invoice, user):
    """Backward-compatible wrapper for the central accounting service."""
    invoice.created_by = user
    return AccountingService.post_fiscal_invoice(invoice)
