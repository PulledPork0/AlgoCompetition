
from .tracked_number import (coerce_int, TrackedNumber)
from math import log

class CostTracking:
    def __init__(self):
        self._last = 0
        self.cost = 0
        # details on fundemental operations
        self.num_add = 0
        self.num_sub = 0
        self.num_mul = 0
        self.num_div = 0
        self.cost_add = 0
        self.cost_sub = 0
        self.cost_mul = 0
        self.cost_div = 0
        # details on algorithms/routines
        self.num_routine = {}
        self.cost_routine = {}

    def NewNumber(self, value=0):
        """obtain a new cost tracked number which uses this cost tracking"""
        return TrackedNumber(self, value)

    def last(self):
        """cost since last asked (convenient for loops)"""
        diff = self.cost - self._last
        self._last = self.cost
        return diff

    def summary(self):
        total = float(self.cost)
        s  =  "total cost: {} ({:.2e})\n".format(self.cost, total)
        s += ("basic operation counts:\n"
              "    add:{:.2e}, sub:{:.2e}, mul:{:.2e}, div:{:.2e}\n".format(
                self.num_add, self.num_sub, self.num_mul, self.num_div))
        s += ("basic operation costs:\n"
              "    add:{:.2e}, sub:{:.2e}, mul:{:.2e}, div:{:.2e}\n".format(
                self.cost_add, self.cost_sub, self.cost_mul, self.cost_div))
        if len(self.num_routine):
            algo_names = [name for name in self.num_routine]
            algo_names.sort()
            count_details = []
            cost_details = []
            for name in algo_names:
                count = self.num_routine[name]
                cost = self.cost_routine[name]
                count_details.append("{}:{:.2e}".format(name, count))
                cost_details.append("{}:{:.2e} ({:.1f}%)".format(
                                    name, cost, (100.0*cost)/total))
            s += "routine counts:\n"
            s += "    {}\n".format(", ".join(count_details))
            s += "routine costs (percent of total):\n"
            s += "    {}\n".format(", ".join(cost_details))
        return s


    # --- a normal user should not need to use the routines below directly ---
    # they are the necessary interface for a number-like object to hook into
    # the cost tracking

    # Don't care too much about the specifics of costs:
    #   1) should be independent of hardware / architecture details
    #   2) willing to ignore the cost of math on constants, as natural
    #       constants appearing in algorithms are usually small
    #   3) primarily want div > mul > add,sub
    #       and for there to be no silly/hacky incentives to
    #       unroll muls as adds, or divs as subtracts, etc.
    # That is, the goal is to have the costs reasonable enough
    # that people write the algorithms naturally, and then for them
    # to be ranked mostly by (div, mul, add+sub).

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

    def routine_start(self, name):
        # the actual routine/algorithm calculate the cost
        # so costs will also be counted in add,mul,etc.
        if name not in self.num_routine:
            self.num_routine[name] = 1
            self.cost_routine[name] = 0
        else:
            self.num_routine[name] += 1

    def routine_stop(self, name, initial):
        self.cost_routine[name] += self.cost - initial


# -- Helpers for tracking cost of routines

def routine_tracking_start(name, *var_list):
    """
    Starts cost tracking for a routine if any of the variables
    are a TrackedNumber.

    returns tracking_data which should be given to 'routine_tracking_stop'
    to add the cost of the routine.
    """
    for var in var_list:
        if isinstance(var, TrackedNumber):
            ct = var.costTracking
            break
    else:
        return (name, None, 0)
    ct.routine_start(name)
    return (name, ct, ct.cost)

def routine_tracking_stop(tracking_data):
    name, ct, initial = tracking_data
    if ct:
        ct.routine_stop(name, initial)

