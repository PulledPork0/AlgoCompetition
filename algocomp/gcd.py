
from .tracked_number import TrackedNumber
from .cost_tracking import (gcd_tracking_start, gcd_tracking_stop)


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    tracking = gcd_tracking_start(a, b)

    """
    Extended Euclicean algorithm:

    let a0, b0 be the original values of a,b

    at the start of each loop we have
        x0 a0 + y0 b0 = b
        x1 a0 + y1 b0 = a

    then find q=b//a, r=b%a so that
        b = q a + r

    therefore we can get a new equation
              x0 a0 + y0 b0 = b
        - q ( x1 a0 + y1 b0 = a )
        --------------------------
        (x0 - q x1) a0 + (y0 - q y1) b0 = b - qa = r

    using this, new constants can be chosen for the next iteration
        x0' a0 + y0' b0 = b'   <---->   x1 a0 + y1 b0 = a
        x1' a0 + y1' b0 = a'   <---->   (x0 - q x1) a0 + (y0 - q y1) b0 = r

    as r < |a| and r <= |b|, each iteration reduces a,
    and must eventually converge on a=0.
    This means we have:
        x0 a0 + y0 b0 = b
        x1 a0 + y1 b0 = 0
    The gcd(b,0) = |b|, so we cannot reduce further.
    And due to construction gcd(x0,y0)=1, so we have
        x0 a0 + y0 b0 = b = +/-gcd(a0,b0)
    So if b is negative, flip the signs of b,x0,y0.

    Return (b,x0,y0) which relate by: x0 a0 + y0 b0 = b = gcd(a0,b0).
    """

    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
        b, a = a, r

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

