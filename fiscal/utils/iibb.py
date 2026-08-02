def calculate_iibb(customer, subtotal):
    profile = customer.tax_profile

    if profile.iibb_status != "INSCRIPTO":
        return 0

    return subtotal * profile.iibb_percentage
