
"""
-- Example Entry #2 --

This example demonstrates use of the optional setup routine.

The setup routine is called once at the start of each testing round.
It should construct a cube with the provided discriminant such that:
  (A1, B1, C1) = (A2, B2, C2) = (2, 1, (1-discriminant)//8)
It returns this initial cube along with an arbitrary "info" object that can be
used to store one-time calculated values or any other information you desire.
"""

from algocomp import *


def setup(discriminant):
    L = isqrt(isqrt(-discriminant//4))
    info = {"D":discriminant, "L":L}
    cube = construct_nudupl_cube(2, 1, (1-discriminant)//8, L)
    return (cube, info)


def run(cube, info):
    """
    1) get the forms, and then just forget the original cube values
    2) reduce the form that needs squaring
    3) construct a new cube from scratch using a nudupl like algorithm
        which partially reduces the cube
    """
    a,b,c,d,e,f,g,h = cube

    # Because we are guaranteed (A1,B1,C1) = (A2,B2,C2)
    #   the equations show b=e, d=g.
    # Therefore we can slightly simplify the B3 form equations.
    assert b == e
    assert d == g

    # A3 = b*e - a*f
    A3 = b*b - a*f

    # B3 = -a*h + b*g - c*f + d*e
    B3 = -a*h - c*f + 2*b*d

    # C3 = d*g - c*h
    C3 = d*d - c*h

    A, B, C = reduce_form(A3, B3, C3)

    new_cube = construct_nudupl_cube(A, B, C, info["L"])

    if 0:
        # silly test, apply some arbitrary transformation to the cube
        new_cube = transform_cube(new_cube, 7,3,2,1)

    return new_cube

