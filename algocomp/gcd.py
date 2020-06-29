
from .tracked_number import (TrackedNumber, coerce_int)
from .cost_tracking import (gcd_tracking_start, gcd_tracking_stop)


def xgcd(a, b):
    """
    return (g, x, y) such that a x + b y = g = gcd(a, b)

    ---
    Extended Euclicean algorithm:

    let a0, b0 be the original values of a,b
    initialize
        x0 = 0, y0 = 1
        x1 = 1, y1 = 0

    this means initially we have
    (and as will be shown inductively, this is also the case for the start
    of every loop)
        x0 a0 + y0 b0 = b
        x1 a0 + y1 b0 = a
        gcd(a, b) = gcd(a0, b0)
        x0 y1 - y0 x1 = +/-1

    note -- the last relation, from bezout's identity, guarantees that
        gcd(x0, y0) = 1
        gcd(x1, y1) = 1

    loop while a != 0:

    find q=b//a, r=b%a so that
        b = q a + r

    therefore we can get a new equation
              x0 a0 + y0 b0 = b
        - q ( x1 a0 + y1 b0 = a )
        --------------------------
        (x0 - q x1) a0 + (y0 - q y1) b0 = b - qa = r

    using this, new constants can be chosen for the next iteration
        x0' a0 + y0' b0 = b'   <---->   x1 a0 + y1 b0 = a
        x1' a0 + y1' b0 = a'   <---->   (x0 - q x1) a0 + (y0 - q y1) b0 = r
    written out explicitly
        x0' = x1
        y0' = y1
        x1' = x0 - q x1
        y1' = y0 - q y1
        a' = r
        b' = a
    which can be verified to satisfy the other loop invariants
        gcd(a', b') = gcd(r, a) = gcd(r + qa, a) = gcd(b, a) = gcd(a0, b0)
        x0' y1' - y0' x1' = x1 (y0 - q y1) - y1 (x0 - q x1)
                          = -(x0 y1 - y0 x1) = -/+ 1

    repeat loop

    Analysis:
    As |r| < |a| and |r| <= |b|, each iteration reduces |a|,
    and must eventually converge on a=0 (our exit condition).
    This means we will reach:
        x0 a0 + y0 b0 = b
        x1 a0 + y1 b0 = 0
    The gcd(b,0) = |b|, so we cannot reduce further.
    And by construction, gcd(x0,y0)=1 and gcd(a,b)=gcd(a0,b0) so we have
        x0 a0 + y0 b0 = b = +/-gcd(a0,b0)

    Therefore, the only remaining step is to potentially flip the signs
    of the parameters to return gcd always positive:
        if b<0 then flip the signs of b,x0,y0

    Return (b,x0,y0) which relate by: x0 a0 + y0 b0 = b = gcd(a0,b0).
    """
    tracking = gcd_tracking_start(a, b)

    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
        b, a = a, r

    gcd_tracking_stop(tracking)

    if b < 0:
        return (-b, -x0, -y0)
    return (b, x0, y0)


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


def partial_xgcd(a, b, L):
    """
    return (u,x,v,y) such that
      1) u x - v y = a,   with |v| <= L  or  u = 0
      2) gcd(u,v) = gcd(a,b)
      3) gcd(x,y) = 1

    ---
    Partial Euclidean reduction:
    Note that the sign is different that xgcd,
    to match other libraries like flint, and nudupl literature

    let a0, b0 be the original values of a,b
    and use as intial values
        x=1, y=0

    this means initially we have
    (and as will be shown inductively, this is also the case for the start
    of every loop)
        x a - y b = a0
        gcd(a, b) = gcd(a0, b0)
        gcd(x, y) = 1

    loop while a != 0 and |b| > L:

    find q=b//a, r=b%a so that
        b = q a + r

    therefore we can get a new equation
    x a - y (q a + r) = a0
    (x - q y) a - y r = a0
    (-y) r - (q y - x) a = a0

    using this, new constants can be chosen for the next iteration
        x' a' - y' b' = a0   <---->   (-y) r - (q y - x) a = a0
    written out explicitly:
        x' = -y
        y' = q y - x
        a' = r
        b' = a
    which can be verified to satisfy the other loop invariants
        gcd(a', b') = gcd(r, a) = gcd(r + qa, a) = gcd(b, a) = gcd(a0, b0)
        gcd(x', y') = gcd(-y, q y - x) = gcd(y, x) = 1

    repeat loop

    Analysis:
    As |r| < |a| and |r| <= |b|, each iteration reduces |a|
    and after the first, |a| < |b|, so each iteration after the first
    must also reduce |b|.

    This means eventually we will converge on a=0, unless we exit
    early because |b| < L (thus "partial" reduction).

    return the calculated (a,x,b,y) which meet all the required conditions now
    """
    tracking = gcd_tracking_start(a, b)

    a0 = a
    x, y = 1, 0
    while a != 0 and abs(b) > L:
        q, r = divmod(b, a)
        x, y = -y, q*y - x
        a, b = r, a

    assert a*x - b*y == a0

    gcd_tracking_stop(tracking)
    return (a, x, b, y)

