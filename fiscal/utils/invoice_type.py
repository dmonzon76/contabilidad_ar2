def determine_invoice_type(customer):
    cat = customer.tax_profile.afip_category

    if cat == "RI":
        return "A"
    elif cat in ["MONO", "EX", "NR", "MT"]:
        return "C"
    elif cat == "CF":
        return "B"
    else:
        return "C"
