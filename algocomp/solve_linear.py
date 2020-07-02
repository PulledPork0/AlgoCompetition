
from .tracked_number import coerce_int as _int
from .gcd import xgcd
from .int_div import (exact_div, mod_min)


def solve_linear(a,b,c):
    """return (x,y) such that a*x + b*y = c, and |x| minimized"""

    # Start by checking some special cases first
    if a==0:
        if b==0:
            assert c==0
            return (0,0)
        assert (_int(c) % _int(b)) == 0   # use _int to bypass cost for assert
        x = 0
        y = c//b
        return (x,y)

    if b==0:
        assert (_int(c) % _int(a)) == 0   # use _int to bypass cost for assert
        x = c//a
        y = 0
        return (x,y)

    # solve: a u + b v = g = gcd(a,b)
    g,u,v = xgcd(a,b)
    assert (_int(c) % _int(g))==0     # use _int to bypass cost for assert

    """
    given
        a u + b v = g = gcd(a,b)
    then
        a x + b y = c
    has the solution (with a freedom in 'n')
        x = u (c/g) + n b
        y = v (c/g) - n a

    using the freedom in n, we can get the minimal x
        -|b/2| < x <= |b/2|
    according to:
    x = (u c / g) % b
    if abs(x) > abs(b/2):  # basicly, but see mod_min for actual details
        x = x - b

    """

    if g == 1:
        x = mod_min(u*c, b) # note: b=0 already handled in special case
    else:
        x = mod_min(u*(c//g), b) # note: b=0 already handled in special case

    # now with the minimal x, just solve for y
    y = exact_div(c - a*x, b)

    return (x,y)

