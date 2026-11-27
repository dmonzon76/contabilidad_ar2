# sales/models/__init__.py

from customers.models import Customer

from .credit_note import CreditNote
from .sale import Sale
from .sale_item import SaleItem

__all__ = [
    "Customer",
    "Sale",
    "SaleItem",
    "CreditNote"
]

