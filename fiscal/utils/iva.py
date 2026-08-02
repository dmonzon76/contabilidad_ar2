def calculate_iva(lines):
    iva_total = 0
    subtotal = 0

    for line in lines:
        line_subtotal = line.quantity * line.unit_price
        subtotal += line_subtotal

        iva_total += line_subtotal * (line.vat_rate / 100)

    return subtotal, iva_total
