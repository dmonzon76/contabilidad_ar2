# sales/models/__init__.py

from .customer import Customer
from .sale import Sale
from .sale_item import SaleItem

__all__ = [
    "Customer",
    "Sale",
    "SaleItem",
]
