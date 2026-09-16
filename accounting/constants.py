# ============================================================
# ACCOUNTING EVENTS
# ============================================================

class AccountingEvents:

    # ========================================================
    # SALES
    # ========================================================

    SALE_GOODS = "SALE_GOODS"
    SALE_SERVICES = "SALE_SERVICES"

    SALE_CREDIT_NOTE = "SALE_CREDIT_NOTE"
    SALE_DEBIT_NOTE = "SALE_DEBIT_NOTE"

    CUSTOMER_PAYMENT = "CUSTOMER_PAYMENT"

    # ========================================================
    # PURCHASES
    # ========================================================

    PURCHASE_GOODS = "PURCHASE_GOODS"
    PURCHASE_EXPENSE = "PURCHASE_EXPENSE"

    PURCHASE_CREDIT_NOTE = "PURCHASE_CREDIT_NOTE"
    PURCHASE_DEBIT_NOTE = "PURCHASE_DEBIT_NOTE"

    SUPPLIER_PAYMENT = "SUPPLIER_PAYMENT"

    # ========================================================
    # INVENTORY
    # ========================================================

    STOCK_ENTRY = "STOCK_ENTRY"

    STOCK_ADJUSTMENT_POSITIVE = (
        "STOCK_ADJUSTMENT_POSITIVE"
    )

    STOCK_ADJUSTMENT_NEGATIVE = (
        "STOCK_ADJUSTMENT_NEGATIVE"
    )

    # ========================================================
    # TAXES
    # ========================================================

    VAT_PAYMENT = "VAT_PAYMENT"

    PERCEPTIONS_PAYMENT = (
        "PERCEPTIONS_PAYMENT"
    )

    RETENTIONS_PAYMENT = (
        "RETENTIONS_PAYMENT"
    )

    # ========================================================
    # ACCOUNTING
    # ========================================================

    OPENING_ENTRY = "OPENING_ENTRY"

    CLOSING_ENTRY = "CLOSING_ENTRY"
