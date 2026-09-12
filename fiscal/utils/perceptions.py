def calculate_perceptions(customer, subtotal):
    profile = customer.tax_profile

    if not profile.uses_perceptions:
        return 0

    return subtotal * profile.iva_perception_percentage


def calculate_retentions(customer, subtotal):
    profile = customer.tax_profile

    if not profile.uses_retentions:
        return 0

    return subtotal * profile.ganancias_percentage


from decimal import Decimal


def _invoice_subtotal(invoice):
    return sum(line.line_total for line in invoice.lines.all())


def calculate_iibb_perception(amount, rate=None):
    if rate is None:
        amount, rate = _invoice_subtotal(amount), Decimal("0.035")
    return amount * rate


def calculate_iva_perception(amount, rate=None):
    if rate is None:
        amount, rate = _invoice_subtotal(amount), Decimal("0.05")
    return amount * rate


def calculate_rg4815_perception(amount, rate=None):
    if rate is None:
        amount, rate = _invoice_subtotal(amount), Decimal("0.45")
    return amount * rate
