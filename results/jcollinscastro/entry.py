
"""
Copyright (c) 2020 jcollinscastro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# Modified to combine changes all into entry.py

from algocomp import *


def reduce_form(a,b,c):
    """calculates  partially reduced binary quadratic form"""
    a0,b0,c0 = a,b,c

    # -- normalize form --
    if c<a:
        """
        apply matrix
                |0 -1|
                |1  0|
        """
        a, b, c = c, -b, a
    if -a < b <= a:
        """
        This means that (a,b,c) is already reduced
        """
        return (a,b,c)

    tracking = routine_tracking_start("reduce_form", a, b, c)
    #http://mathonline.wikidot.com/reduced-binary-quadratic-forms
    n = (b + a) // (2*a) #  (quotient of b+a by 2a guarantees -a < b - 2*a*n < a) 
    # transform:  a, b, c = a, b - 2*a*n, c - b*n + a*n*n

    # This is the action under the matrix |1 -n|
    #                                     |0  1|
    an = a*n
    b = b - an
    c = c - n*b
    b = b - an

    routine_tracking_stop(tracking)

    return (a,b,c)


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

    return new_cube

