
def exact_div(a, b):
    """
    performs integer division: a/b, with expectation that result is exact
    raises ValueError exception if b does not divide a
    """
    q, r = divmod(a, b)
    if r != 0:
        raise ValueError("dividend is not multiple of divisor")
    return q

