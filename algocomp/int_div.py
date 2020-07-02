
def exact_div(a, b):
    """
    performs integer division: a/b, with expectation that result is exact
    raises ValueError exception if b does not divide a
    """
    q, r = divmod(a, b)
    if r != 0:
        raise ValueError("dividend is not multiple of divisor")
    return q


def divmod_min(a, b):
    """
    return q,r such that a = qb + r, with minimum |r|
    """
    q, r = divmod(a, b)
    
    # we will want to adjust r if
    #   (|r| > |b/2|), which is equivalent to checking
    #   (|2r| > |b|),
    #   (|r| > |b| - |r|)
    # then using the fact that for python,
    # divmod will give |r| < |b|  and  r,b will have the same sign
    #   (|r| > |b - r|)
    diff = b - r
    if abs(r) > abs(diff):
        q = q + 1 
        r = -diff
    return q,r


def mod_min(a, b):
    """
    return r such that r = a (mod b), with minimum |r|
    """
    # like divmod_min, just skipping a single add
    r = (a % b)
    diff = b - r
    if abs(r) > abs(diff):
        r = -diff
    return r


