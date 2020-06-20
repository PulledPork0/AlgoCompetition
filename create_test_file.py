#!/usr/bin/env python3

from inkfish.create_discriminant import create_discriminant
from inkfish.classgroup import ClassGroup
import hashlib
import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=str, default='SomeSeed',
        help="seed phrase, default=%(default)r")
    parser.add_argument('-n', '--ntest', type=int, default=10,
        help="number of test values created, default=%(default)s")
    parser.add_argument('-r', '--rstep', type=int, default=1000,
        help="number of recursive steps during testing, default=%(default)s")
    parser.add_argument('-b', '--bitsize', type=int, default=128,
        help="bitsize of discriminant, default=%(default)s")
    parser.add_argument('fileout', type=str)

    if len(sys.argv)<2:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    with open(args.fileout,"w") as f:
        # first line is unused, description text
        f.write("bitsize:{} rstep:{} ntest:{}\n"
                "".format(args.bitsize, args.rstep, args.ntest))

        # actual parameters for verification purposes
        f.write("{}\n".format(args.seed))
        f.write("{}\n".format(args.rstep))
        
        seedbytes = args.seed.encode("utf8")
        for i in range(args.ntest):
            d = create_discriminant(seedbytes + bytes([i]), args.bitsize)
            form = ClassGroup.from_ab_discriminant(2,1,d)

            # do an initial square, equivalent to setting up the first cube
            form = form.square()

            # repeatedly apply squaring operation the requested number of times
            for _ in range(args.rstep):
                form = form.square()

            a, b, c = form
            f.write("{} {} {} {}\n".format(d, a, b, c))

