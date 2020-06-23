
from .tracked_number import TrackedNumber


def isqrt(n):
    """
    returns floor(sqrt(n))

    uses an initial guess, and Newton's method to converge on the answer

    initial code from:
    https://code.activestate.com/recipes/577821-integer-square-root-function
    https://stackoverflow.com/a/1624602
    """
    if n < 0:
        raise ValueError('square root not defined for negative numbers')
    if isinstance(n, float):
        raise TypeError('float not supported for isqrt as there may not be '
                        'enough precision to get a useful answer')

    """
    we need to refer to bit representation to get initial guess
    we'll count this part cost free for simplicity,
        and because it should be quick
    """
    if n == 0:
        return 0
    a, b = divmod(int(n).bit_length(), 2)
    x = 2**(a+b)
    if isinstance(n, TrackedNumber):
        # return to cost tracking
        x = n.costTracking.NewNumber(x)

    while True:
        y = (x + n//x)//2
        if y >= x:
            return x
        x = y


