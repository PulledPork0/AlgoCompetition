
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

