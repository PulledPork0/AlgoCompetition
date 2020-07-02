
from .tracked_number import coerce_int
from .solve_linear import *
from .gcd import (xgcd, gcd, partial_xgcd)
from .int_div import (exact_div, mod_min)
from .cube import *


def construct_nudupl_cube(A, B, C, L):
    """
    Constructs a cube with (A1,B1,C1)=(A2,B2,C2)=(A,B,C)
    and performs a partial reduction limited by L.

    Assumes we are working with a prime discriminant, so gcd(A,B)=gcd(C,B)=1.

    ---
    Algorithm:

    Initially sets up the faces of the cube like so:
    |a b| = |-1 b|    |e f| = |b f|
    |c d|   | 0 A| ,  |g h|   |A B|

    This garauntees A1=A2=A, B1=B2=B, so only need to constrain C1
    which then sets the discriminant and so the first two forms = (A,B,C).

    C1 = fg - eh = fA - bB = C ... solvable for f,b since gcd(A,B)=1
    """

    # -- construct cube
    a = -1
    c = 0
    d = A
    g = A
    h = B

    # solve -bB + fA = C, with minimal |b|
    b,f = solve_linear(-B,A,C)

    e = b

    """
    -- now partially reduce the cube

    with a matrix |w z| where wx - yz = 1 (and so gcd(x,y)=gcd(w,z)=1)
                  |y x|

    we can transform a cube while maintaining the values of
    form1=(A1,B1,C1) and form2=(A2,B2,C2) but changing form3 by an
    equivalence transformation.

      |w z| |new_a new_b| = |-1 b|
      |y x| |new_c new_d|   | 0 A|

      |w z| |new_e new_f| = |b f|
      |y x| |new_g new_h|   |A B|

    we can also write the new values in terms of the old, using the
    inverse matrix

      |new_a new_b| = | x -z| |-1 b|
      |new_c new_d|   |-y  w| | 0 A|

      |new_e new_f| = | x -z| |b f|
      |new_g new_h|   |-y  w| |A B|

    Note: because initially b=e and d=g, we see this tranformation
          preserves that fact as well: new_b = new_e, new_d = new_g

    as A is the largest value in the cube, focus on that reducing that

        y new_b + x new_d = A

    which can be obtained starting from
        (A) (1) + (b) (0) = A
    and partial reducing --> new_d x + new_b y = A
        new_d, x, new_b, y = partial_xgcd(A, b, L)
            1) new_d x + new_b y = A,  with |new_b| <= L  or  new_d = 0
            2) gcd(new_d, new_b) = gcd(A,b)
            3) gcd(x,y) = 1

    now notice from the matrix equations
        new_a = -x
        new_c = y

    we can now solve for new_f from the linear equations
    the cube values must satisfy:
       new_a C2 + new_f A1 = new_b (B1 + B2)/2
       new_a C + new_f A = new_b B
    thus:
       new_f = (new_b B - new_a C)/A

    we can now solve the new_h from the constraint on C
       C = new_f new_g - new_e new_h
    using new_b = new_e, new_d = new_g
       C = new_f new_d - new_b new_h
    thus:
       new_h = (new_f new_d - C)/new_b
    """

    new_d, x, new_b, y = partial_xgcd(A, b, L)

    if y == 0:
        # special case, y=0, already partially reduced to L
        # this is rare but necessary to check for to prevent
        #   possible division-by-zero in the calculation below

        #print("##### Special case #####, new_b:",new_b)
        return (a,b,c,d,e,f,g,h)

    new_a = -x
    new_c = y

    new_f = exact_div(new_b*B - new_a*C, A)

    # new_b can only be 0 if partial_xgcd performed no steps
    # and that case was already handled in the special case above
    new_h = exact_div(new_f*new_d - C, new_b)

    if 0:
        # debugging

        # new_b = b*x - z*A  --->  z = (b*x-new_b)/A
        z = exact_div(b*x - new_b, A)

        # w*x - y*z = 1  --->  w = (1 + y*z)/x
        # ... nope, sometimes x is 0
        #
        # new_d = -y*b + w*A  --->  w = (new_d + b*y)/A
        w = exact_div(new_d + b*y, A)

        assert w*x - y*z == 1
        print("----- initial nudupl cube")
        initial_cube = (a, b, c, d, b, f, d, h)
        reduced_cube = (new_a, new_b, new_c, new_d, new_b, new_f, new_d, new_h)
        print_cube_stats(initial_cube)
        print("new_d:{}, x:{}, new_b:{}, y:{}".format(new_d,x,new_b,y))
        print("transformation:")
        print("  x:{}, -z:{}, -y:{}, w:{}".format(x,-z,-y,w))
        check_cube = transform_cube(initial_cube, x,-z,-y,w)
        assert check_cube == reduced_cube
        print_cube_stats(reduced_cube)

    return (new_a, new_b, new_c, new_d, new_b, new_f, new_d, new_h)

