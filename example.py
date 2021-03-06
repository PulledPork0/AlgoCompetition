
from algocomp import *

def run(cube, info):
    """
    as an example starting point:

    This just gets the (A3,B3,C3) form and then completely tosses the
    original cube.

    Then reduce the form (use equivalence to obtain form with smaller
    magnitude numbers) so the values don't grow without bound each step.

    then calculates an entirely new cube for these forms
    """
    a,b,c,d,e,f,g,h = cube
    A3 = b*e - a*f
    B3 = -a*h + b*g - c*f + d*e
    C3 = d*g - c*h

    A,B,C = reduce_form(A3, B3, C3)

    """
    Assumes we are working with a prime discriminant, so gcd(A,B)=gcd(C,B)=1

    Sets up the faces of the new cube like so:
    |a b| = |-1 b|    |e f| = |b f|
    |c d|   | 0 A| ,  |g h|   |A B|

    Which only has two unknowns: b,f

    From the cube equations:
      bc - ad = A1
      ce - ag = A2
      cf - ah = (B1 + B2)/2
      bg - de = (B1 - B2)/2
      fg - eh = C1
      df - bh = C2

    We can see that this setup of the new cube guarantees A1=A2=A, B1=B2=B.
    As a solution to the cube equations also has:
        B1^2 - 4 A1 C1 = B2^2 - 4 A2 C2 = discriminant
    We just need to find the values b,f which set C1 = C, and this will
    make the first two forms = (A,B,C).

    C1 = fg - eh = fA - Bb = C
    And this will always be solvable for b,f because the additional
    guarantees of the contest puzzle allow us to know gcd(A,B) = 1.
    """

    # initialize most of the cube
    a = -1
    c = 0
    d = A
    g = A
    h = B

    # solve:  A f - B b = C
    f,b = solve_linear(A,-B,C)

    e = b

    if 0:
        # show debug info each step
        outA3 = b*e - a*f
        outB3 = -a*h + b*g - c*f + d*e
        outC3 = d*g - c*h
        outA, outB, outC = reduce_form(outA3, outB3, outC3)
        print("in:({},{},{}) reduced:({},{},{}) --> "
              "out:({},{},{}) reduced:({},{},{})".format(
              A3,B3,C3, A,B,C, outA3,outB3,outC3, outA,outB,outC))

    return (a,b,c,d,e,f,g,h)

