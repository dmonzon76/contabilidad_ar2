from .electronic_voucher_book import (
    electronic_voucher_book_list,
    electronic_voucher_book_create,
    electronic_voucher_book_edit,
    electronic_voucher_book_delete,
)
from .fiscal_invoice import (
    fiscal_invoice_list,
    fiscal_invoice_create,
    fiscal_invoice_edit,
)

from .fiscal_invoice_line import fiscal_invoice_line_create

from .fiscal_product import (
    fiscal_product_list,
    fiscal_product_create,
    fiscal_product_edit,
)

from .fiscal_service import (
    fiscal_service_list,
    fiscal_service_create,
    fiscal_service_edit,
)

from .fiscal_sale import (
    fiscal_sale_list,
    fiscal_sale_create,
    fiscal_sale_generate_invoice,
)
