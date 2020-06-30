
from .tracked_number import coerce_int
from .solve_linear import *


def print_cube_stats(cube):
    """for debugging: given a cube as a tuple of 8 values, print some stats"""

    # extract ints, so none of this gets counted in cost
    a,b,c,d,e,f,g,h = [coerce_int(x) for x in cube]

    print('-'*40)
    print('a={} b={} c={} d={} e={} f={} g={} h={}'.format(a,b,c,d,e,f,g,h))
    A1 = (b*c - a*d)
    B1 = (- a*h + b*g + c*f - d*e)
    C1 = (f*g - e*h)
    # due to construction, all discriminants have to be the same
    print('disc = {}'.format(B1*B1 - 4*A1*C1))
    print('A1 = {}'.format(A1))
    print('B1 = {}'.format(B1))
    print('C1 = {}'.format(C1))
    print(' A2 = {}'.format(c*e -a*g))
    print(' B2 = {}'.format(-a*h -b*g +c*f +d*e))
    print(' C2 = {}'.format(d*f -b*h))
    print('A3 = {}'.format(b*e - a*f))
    print('B3 = {}'.format(-a*h +b*g -c*f +d*e))
    print('C3 = {}'.format(d*g - c*h))
    print(' (B1+B2)/2 = {}'.format(-a*h +c*f))
    print(' (B1-B2)/2 = {}'.format(b*g -d*e))


def get_cube_with_squared_form(A, B, C):
    """
    Assumes we are working with a prime discriminant, so gcd(A,B)=gcd(C,B)=1.

    Sets up the faces of the cube like so:
    |a b| = |-1 b|    |e f| = |b f|
    |c d|   | 0 A| ,  |g h|   |A B|

    This garauntees A1=A2=A, B1=B2=B, so only need to constrain C1
    which then sets the discriminant and so the first two forms = (A,B,C).

    C1 = fg - eh = fA - bB = C ... solvable for f,b since gcd(A,B)=1
    """

    a = -1
    c = 0
    d = A
    g = A
    h = B

    f,b = solve_linear(A,-B,C)
    e = b

    return (a,b,c,d,e,f,g,h)


def default_initial_cube(disc):
    """return (cube, extra_info)"""
    cube = get_cube_with_squared_form(2, 1, (1-disc)//8)
    return (cube, None)

