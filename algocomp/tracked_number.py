
from .ipow import ipow


def coerce_int(x):
    if isinstance(x, TrackedNumber):
        return x.value
    if isinstance(x, int):
        return x
    raise TypeError("Got type {}, expected TrackedNumber or int"
                    "".format(x.__class__.__name__))


class TrackedNumber:
    def __init__(self, costTracking, value=0):
        if not isinstance(value, int):
            raise TypeError("value is type {}, expected TrackedNumber or int"
                            "".format(value.__class__.__name__))
        self.costTracking = costTracking
        self.value = value

    def copy(self):
        return TrackedNumber(self.costTracking, self.value)


    def _check_coerce_int(self, x):
        if isinstance(x, TrackedNumber):
            if self.costTracking != x.costTracking:
                raise ValueError("values have mismatched cost tracking")
        return coerce_int(x)


    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "TrackedNumber(value={})".format(self.value)


    # unary operations

    # -- this can unintentially allow removing tracking,
    #    explicitly use .value instead
    #def __int__(self):
    #    return self.value

    def __bool__(self):
        return self.value != 0

    def __neg__(self):
        return TrackedNumber(self.costTracking, -self.value)

    def __pos__(self):
        return TrackedNumber(self.costTracking, +self.value)

    def __abs__(self):
        return TrackedNumber(self.costTracking, abs(self.value))


    # comparisons

    def __eq__(self, other):
        return self.value == coerce_int(other)

    def __ge__(self, other):
        return self.value >= coerce_int(other)

    def __gt__(self, other):
        return self.value > coerce_int(other)

    def __le__(self, other):
        return self.value <= coerce_int(other)

    def __lt__(self, other):
        return self.value < coerce_int(other)

    def __ne__(self, other):
        return self.value != coerce_int(other)


    # basic arithmetic

    def __add__(self, other):
        x,y = self.value, self._check_coerce_int(other)
        self.costTracking.add(x,y)
        return TrackedNumber(self.costTracking, x+y)

    def __sub__(self, other):
        x,y = self.value, self._check_coerce_int(other)
        self.costTracking.sub(x,y)
        return TrackedNumber(self.costTracking, x-y)

    def __mul__(self, other):
        x,y = self.value, self._check_coerce_int(other)
        self.costTracking.mul(x,y)
        return TrackedNumber(self.costTracking, x*y)

    # -- this no longer supported
    # issue:
    #   a/b will give a float when a and b are int, even if b divides a
    #
    # As the point is to be able to use these objects mixed with ints
    # without worry, this operator must therefore be discouraged.
    #
    # use "exact_div" function if you want to denote a division is
    # an exact division and assert check that it is
    #
    #def __truediv__(self, other):
    #    x,y = self.value, self._check_coerce_int(other)
    #    q, r = divmod(x,y)
    #    if r != 0:
    #        raise ValueError("dividend is not multiple of divisor")
    #    self.costTracking.div(x,y)
    #    return TrackedNumber(self.costTracking, x//y)

    def __floordiv__(self, other):
        x,y = self.value, self._check_coerce_int(other)
        self.costTracking.div(x,y)
        return TrackedNumber(self.costTracking, x//y)

    def __mod__(self, other):
        x,y = self.value, self._check_coerce_int(other)
        self.costTracking.div(x,y)
        return TrackedNumber(self.costTracking, x%y)

    def __divmod__(self, other):
        x,y = self.value, self._check_coerce_int(other)
        self.costTracking.div(x,y)
        return (TrackedNumber(self.costTracking, x//y),
                TrackedNumber(self.costTracking, x%y))


    def __radd__(self, other):
        x,y = self._check_coerce_int(other), self.value
        self.costTracking.add(x,y)
        return TrackedNumber(self.costTracking, x+y)

    def __rsub__(self, other):
        x,y = self._check_coerce_int(other), self.value
        self.costTracking.sub(x,y)
        return TrackedNumber(self.costTracking, x-y)

    def __rmul__(self, other):
        x,y = self._check_coerce_int(other), self.value
        self.costTracking.mul(x,y)
        return TrackedNumber(self.costTracking, x*y)

    # -- no longer supported
    # see notes under truediv for details
    #def __rtruediv__(self, other):
    #    x,y = self._check_coerce_int(other), self.value
    #    q, r = divmod(x,y)
    #    if r != 0:
    #        raise ValueError("dividend is not multiple of divisor")
    #    self.costTracking.div(x,y)
    #    return TrackedNumber(self.costTracking, x//y)

    def __rfloordiv__(self, other):
        x,y = self._check_coerce_int(other), self.value
        self.costTracking.div(x,y)
        return TrackedNumber(self.costTracking, x//y)

    def __rmod__(self, other):
        x,y = self._check_coerce_int(other), self.value
        self.costTracking.div(x,y)
        return TrackedNumber(self.costTracking, x%y)

    def __rdivmod__(self, other):
        x,y = self._check_coerce_int(other), self.value
        self.costTracking.div(x,y)
        return (TrackedNumber(self.costTracking, x//y),
                TrackedNumber(self.costTracking, x%y))

    # exponentiation
    #   included for completeness, but probably only need square
    #   which would be simpler to just write as x*x

    def __pow__(self, other):
        return ipow(self, other)

    def __rpow__(self, other):
        return ipow(other, self)

