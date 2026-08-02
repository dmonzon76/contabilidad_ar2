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
