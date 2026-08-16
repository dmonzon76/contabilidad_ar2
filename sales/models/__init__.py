# sales/models/__init__.py

from .customer import Customer
from .sale import Sale
from .sale_item import SaleItem

from .invoice import Invoice
from .invoice_line import InvoiceLine

__all__ = [
    "Customer",
    "Sale",
    "SaleItem",
    "Invoice",
    "InvoiceLine",
]
