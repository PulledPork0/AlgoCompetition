
from .tracked_number import TrackedNumber
from .cost_tracking import (gcd_tracking_start, gcd_tracking_stop)


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    tracking = gcd_tracking_start(a, b)

    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1

    gcd_tracking_stop(tracking)

    if b >= 0:
        return b, x0, y0
    return -b, -x0, -y0


def gcd(a, b):
    tracking = gcd_tracking_start(a, b)

    if abs(a)>abs(b):
        a,b = b,a
    while a != 0:
        a,b = (b%a), a

    gcd_tracking_stop(tracking)
    return b


def mod_inverse(x, M):
    """solve ax + My = 1, so ax = 1 (mod M)"""
    g, a, b = xgcd(x,M)
    assert g==1
    return a


def partial_reduce(a, b, L):
    """return (a,b) such that abs(a)<abs(b)<L or a=0"""

    # even though this is a "partial gcd", still include it in stats
    tracking = gcd_tracking_start(a, b)

    if abs(a)>abs(b):
        a,b = b,a
    while a != 0 and abs(b)>=L:
        a,b = (b%a), a

    gcd_tracking_stop(tracking)
    return a,b


# NOTE: not much thought was put into solve_linear
#       should probably follow up on it

def solve_linear(a,b,c):
    """return (x,y) such that a*x + b*y = c"""

    # It would be nice to have a, in some sense, "minimal" solution.
    # unsure if there is a nicer / more uniform was of handling this

    # Start by checking some special cases first
    if a==0:
        if b==0:
            assert c==0
            return (0,0)
        assert (int(c) % int(b))==0   # use int to bypass cost for assert
        x = 0
        y = c//b
        return (x,y)

    if b==0:
        assert (int(c) % int(a))==0   # use int to bypass cost for assert
        x = c//a
        y = 0
        return (x,y)

    if abs(a) > abs(b):
        if (c%a)==0:
            return (c//a, 0)
        if (c%b)==0:
            return (0, c//b)
    else:
        if (c%b)==0:
            return (0, c//b)
        if (c%a)==0:
            return (c//a, 0)

    g,x,y = xgcd(a,b)
    assert (int(c) % int(g))==0     # use in to bypass cost for assert

    # Is there a more direct way to get the "minimal" solution?
    # this creates a large answer, and then reduces it
    c = (c//g)
    x *= c
    y *= c

    # There is still some freedom
    # x -> x - bn, y -> y + an
    # use this to reduce the answer
    if abs(b)<abs(a):
        n = x//b
        x -= n*b
        y += n*a
    else:
        n = y//a
        x += n*b
        y -= n*a

    return (x,y)


