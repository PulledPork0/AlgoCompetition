
from inkfish.classgroup import ClassGroup
from algocomp import *

def run(a,b,c,d,e,f,g,h):
    """
    as an example starting point,
    this just gets the forms and tosses the original cube

    then reduces the form
    then calculated a new cube for these forms
    """
    A3 = b*e - a*f
    B3 = -a*h + b*g - c*f + d*e
    C3 = d*g - c*h

    form = ClassGroup(A3, B3, C3)
    A, B, C = form.reduced()
    
    """
    Assumes we are working with a prime discriminant, so gcd(A,B)=gcd(C,B)=1

    Sets up the faces of the cube like so:
    |a b| = |-1 b|    |e f| = |b f|
    |c d|   | 0 A| ,  |g h|   |A B|

    This garauntees A1=A2=A, B1=B2=B, so only need to constrain C1
    which then sets the discriminant and so the first two forms = (A,B,C)

    Af - Bb = C ... solvable since gcd(A,B)=1
    """

    a = -1
    c = 0
    d = A
    g = A
    h = B

    f,b = solve_linear(A,-B,C)
    e = b

    if 0:
        # show debug info each step
        outA3 = b*e - a*f
        outB3 = -a*h + b*g - c*f + d*e
        outC3 = d*g - c*h
        form = ClassGroup(outA3, outB3, outC3)
        outA, outB, outC = form.reduced()
        print("in:({},{},{}) reduced:({},{},{}) --> "
              "out:({},{},{}) reduced:({},{},{})".format(
              A3,B3,C3, A,B,C, outA3,outB3,outC3, outA,outB,outC))

    return (a,b,c,d,e,f,g,h)

