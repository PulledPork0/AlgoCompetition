
from .cost_tracking import (routine_tracking_start, routine_tracking_stop)
from .tracked_number import coerce_int as _int


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
    tracking = routine_tracking_start("gcd", a, b)

    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
        b, a = a, r

    routine_tracking_stop(tracking)

    if b < 0:
        return (-b, -x0, -y0)
    return (b, x0, y0)


def gcd(a, b):
    tracking = routine_tracking_start("gcd", a, b)

    if abs(a)>abs(b):
        a,b = b,a
    while a != 0:
        a,b = (b%a), a

    routine_tracking_stop(tracking)
    if b < 0:
        return -b
    return b


def mod_inverse(x, M):
    """solve ax + My = 1, so ax = 1 (mod M)"""
    g, a, b = xgcd(x,M)
    assert g==1
    return a


def partial_xgcd(a, b, L):
    """
    Partial Euclidean reduction
    return (u,x,v,y) such that
      1) u x + v y = a,   with |v| <= L  or  u = 0
      2) gcd(u,v) = gcd(a,b)
      3) gcd(x,y) = 1

    More precisely, there is guaranteed to be a matrix M such that
        det(M) = 1
    and
        [u  v] = [a  b] M

    Note: this uses a positive sign convention like xgcd. This differs from
    the sign convention in some literature and libraries such as Flint.

    ---
    Algorithm

    use as intial values
        u=a, x=1, v=b, y=0

    this means initially we have
    (and as will be shown inductively, this is also the case for the start
    of every loop)
        u x + v y = a
        gcd(u, v) = gcd(a, b)
        gcd(x, y) = 1

    loop while u != 0 and |v| > L:

    find q=v//u, r=v%u so that
        v = q u + r

    therefore we can get a new equation
        u x + (q u + r) y = a
        u (x + q y) + r y = a
        r y + u (x + q y) = a

    using this, new constants can be chosen for the next iteration
        u' x' + v' y' = a   <---->   (-r) (-y) + (u) (x + q y) = a
    the additional negations are so the transformation each
    step have a determinant of one
        |x'| = |0 -1| |x|       |u'| = |q -1| |u|
        |y'|   |1  q| |y|       |v'|   |1  0| |v|

    written out explicitly:
        x' = -y
        y' = x + q y
        u' = -r
        v' = u
    which can be verified to preserve the other loop invariants
        gcd(u', v') = gcd(-r, u) = gcd(-r - qu, u) = gcd(-v, u) = gcd(a, b)
        gcd(x', y') = gcd(-y, x + q y) = gcd(y, x) = 1

    repeat loop

    Analysis:
    As |r| < |u| and |r| <= |v|, each iteration reduces |u|.
    And after the first step |u| < |v|, so each iteration after the first
    must also reduce |v|.

    This means eventually we will converge on u=0, unless we exit
    early because |v| < L (thus "partial" reduction).

    return the calculated (u,x,v,y) which meet all the required conditions now
    """
    tracking = routine_tracking_start("p_gcd", a, b)

    u, x, v, y = a, 1, b, 0
    nstep = 0
    while u != 0 and abs(v) > L:
        # get v = qu + r, with minimum |r|
        # we will want to adjust r if
        #   (|r| > |u/2|), which is equivalent to checking
        #   (|2r| > |u|),
        #   (|r| > |u| - |r|)
        # then using the fact that for python,
        # divmod will give |r| < |u|  and  r,u will have the same sign
        #   (|r| > |u - r|)
        q, r = divmod(v, u)
        diff = u - r
        if abs(r) > abs(diff):
            q = q + 1
            r = -diff

        # update variables
        x, y = -y, x + q*y
        u, v = -r, u
        nstep += 1
    assert _int(u)*_int(x) + _int(v)*_int(y) == a

    if 0:
        # print detailed info on partial_xgcd
        def nbit(x):
            return _int(x).bit_length()
        print("nstep={}  a:{}, b:{}  -->  u:{}, x:{}, v:{}, y:{}".format(
                nstep, nbit(a), nbit(b), nbit(u), nbit(x), nbit(v), nbit(y)))

    routine_tracking_stop(tracking)
    return (u, x, v, y)

