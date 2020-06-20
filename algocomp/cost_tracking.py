
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

    def NewNumber(self, value=0):
        return TrackedNumber(self, value)

    def last(self):
        """cost since last asked (convenient for loops)"""
        diff = self.cost - self._last
        self._last = self.cost
        return diff

    def summary(self):
        return ("total cost:{}, add:{}, sub:{}, mul:{}, div:{}, gcd:{}"
                "".format(self.cost, self.num_add, self.num_sub, self.num_mul,
                          self.num_div, self.num_gcd))


    # Don't care too much about the specifics of costs
    #   want gcd > div > mul > add,sub
    #   and for there to be no silly/hacky incentives to
    #   unroll muls as adds, or divs as subtracts, etc.
    # That is, the goal is to have the costs reasonable enough
    # that people write the algorithms naturally, and then for them
    # to be ranked mostly by (bezout, div, mul, add+sub).

    def add(self, x, y):
        # O(n)
        self.cost += max(x.bit_length(), y.bit_length())
        self.num_add += 1

    def sub(self, x, y):
        # O(n)
        self.cost += max(x.bit_length(), y.bit_length())
        self.num_sub += 1

    def mul(self, x, y):
        # ~ Karatsuba algorithm
        #   nbit x nbit takes O(n^1.6)
        #   unsure what constants to use
        bits = float(x.bit_length() + y.bit_length())
        w = bits**1.6
        self.cost += int(w)
        self.num_mul += 1

    def div(self, x, y):
        # ~ Burnikel-Ziegler divide-and-conquer division
        #  nbit / nbit takes O( M(n) log n )
        bits = float(x.bit_length() + y.bit_length())
        w = log(bits) * (bits**1.6)
        self.cost += int(w)
        self.num_div += 1

    def gcd(self, x, y):
        # let actual algorithm calculate the cost
        self.num_gcd += 1

