#!/usr/bin/env python3

from inkfish.classgroup import ClassGroup
from algocomp import *
import importlib
import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Test algorithm. Example usage: ./run_test.py example")
    parser.add_argument('-t', '--testfile', type=str, default='test128.txt',
        help="file with testing data, default=%(default)r")
    parser.add_argument('algorithm', type=str,
        help="this is imported as a python module and should supply "
             "the function 'run'")

    if len(sys.argv)<2:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.algorithm.endswith(".py"):
        args.algorithm = args.algorithm[:-3]
    m = importlib.import_module(args.algorithm)

    costTracking = CostTracking()

    with open(args.testfile,"r") as f:
        description = f.readline().rstrip()
        print("Description:",description)
        seed = f.readline()[:-1]
        print("Seed: {!r}".format(seed))
        rsteps = int(f.readline())
        ntest = 0
        npass = 0
        for line in f:
            ntest += 1
            disc, A, B, C = [int(s) for s in line.strip().split(' ')]

            cube = get_initial_cube(disc, costTracking)
            for _ in range(rsteps):
                cube = m.run(*cube)
            test_cost = costTracking.last()

            a, b, c, d, e, f, g, h = [int(x) for x in cube]
            A3 = b*e - a*f
            B3 = -a*h + b*g - c*f + d*e
            C3 = d*g - c*h

            if (rsteps%2) == 0:
                B3 = -B3  # correct sign flip parity

            out_disc = B3*B3 - 4*A3*C3

            if out_disc != disc:
                print("FAIL: test {} did not have correct discriminant"
                      "".format(ntest))
            else:
                form = ClassGroup(A3, B3, C3).reduced()
                outA, outB, outC = form
                if outA != A or outB != B or outC != C:
                    print("FAIL: test {} result is incorrect".format(ntest))
                else:
                    print("PASS: test {} passed with cost {}"
                          "".format(ntest, test_cost))
                    npass += 1
            costTracking.last()
    print("passed {} of {} tests".format(npass,ntest))
    print(costTracking.summary())

