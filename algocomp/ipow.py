
def ipow(a,b):
    """
    returns pow(a,b) for integers

    constructed in terms of lower arithmetic to be compatible
    with cost calculations
    """

    # quick special cases
    if b == 0:
        return 1
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == -1:
        if (b%2) == 1:
            return -1
        return 1
    if b < 0:
        raise ValueError('ipow not defined for negative exponent and |base|>1')

    val = 1
    while True:
        b,bit = divmod(b,2)
        if bit:
            val = val*a   # no *= to allow cost calculation
        if b == 0:
            break
        a = a*a   # no *= to allow cost calculation

    return val

