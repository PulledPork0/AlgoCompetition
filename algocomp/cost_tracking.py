
from .tracked_number import TrackedNumber
from math import log

class CostTracking:
    def __init__(self):
        self._last = 0
        self.cost = 0
        self.num_add = 0
        self.num_sub = 0
        self.num_mul = 0
        self.num_div = 0
        self.num_gcd = 0
        self.cost_add = 0
        self.cost_sub = 0
        self.cost_mul = 0
        self.cost_div = 0
        self.cost_gcd = 0

    def NewNumber(self, value=0):
        return TrackedNumber(self, value)

    def last(self):
        """cost since last asked (convenient for loops)"""
        diff = self.cost - self._last
        self._last = self.cost
        return diff

    def summary(self):
        return ("total cost:{}\n"
                "operation counts: add:{}, sub:{}, mul:{}, div:{}, gcd:{}\n"
                "operation costs: add:{}, sub:{}, mul:{}, div:{}, gcd:{}\n"
                "".format(self.cost,
                    self.num_add, self.num_sub, self.num_mul, self.num_div,
                        self.num_gcd,
                    self.cost_add, self.cost_sub, self.cost_mul, self.cost_div,
                        self.cost_gcd))


    # Don't care too much about the specifics of costs
    #   want gcd > div > mul > add,sub
    #   and for there to be no silly/hacky incentives to
    #   unroll muls as adds, or divs as subtracts, etc.
    # That is, the goal is to have the costs reasonable enough
    # that people write the algorithms naturally, and then for them
    # to be ranked mostly by (gcd, div, mul, add+sub).

    def add(self, x, y):
        # O(n)
        c = max(x.bit_length(), y.bit_length())
        self.num_add += 1
        self.cost_add += c
        self.cost += c

    def sub(self, x, y):
        # O(n)
        c = max(x.bit_length(), y.bit_length())
        self.num_sub += 1
        self.cost_sub += c
        self.cost += c

    def mul(self, x, y):
        # ~ Karatsuba algorithm
        #   nbit x nbit takes O(n^1.6)
        #   unsure what constants to use
        bits = float(x.bit_length() + y.bit_length())
        c = int(bits**1.6)
        self.num_mul += 1
        self.cost_mul += c
        self.cost += c

    def div(self, x, y):
        # ~ Burnikel-Ziegler divide-and-conquer division
        #  nbit / nbit takes O( M(n) log n )
        bits = float(x.bit_length() + y.bit_length())
        c = int( log(bits) * (bits**1.6) )
        self.num_div += 1
        self.cost_div += c
        self.cost += c

    def gcd_start(self, x, y):
        # the actual algorithm calculate the cost
        # so costs from gcd will also be counted in add,mul,etc.
        pass

    def gcd_stop(self, initial):
        self.num_gcd += 1
        self.cost_gcd += self.cost - initial


# -- Helpers for tracking cost of gcd

def gcd_tracking_start(a, b):
    if isinstance(a, TrackedNumber):
        ct = a.costTracking
    elif isinstance(b, TrackedNumber):
        ct = b.costTracking
    else:
        return (None, 0)
    ct.gcd_start(int(a), int(b))
    return (ct, ct.cost)

def gcd_tracking_stop(tracking):
    ct, initial = tracking
    if ct:
        ct.gcd_stop(initial)

