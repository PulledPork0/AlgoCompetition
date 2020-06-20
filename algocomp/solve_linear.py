
from .gcd import xgcd


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


