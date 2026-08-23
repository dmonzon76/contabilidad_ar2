# suppliers/utils.py
def validate_cuit(cuit: str) -> bool:
    """
    Valida CUIT/CUIL sin guiones. Devuelve True si es válido.
    """
    if not cuit or len(cuit) != 11 or not cuit.isdigit():
        return False
    mult = [5,4,3,2,7,6,5,4,3,2]
    digits = list(map(int, cuit))
    s = sum([a*b for a,b in zip(mult, digits[:10])])
    mod = 11 - (s % 11)
    if mod == 11:
        mod = 0
    if mod == 10:
        return False
    return mod == digits[10]
