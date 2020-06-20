#!/usr/bin/python3

import sys


def load(path):
    out = {}
    with open(path) as f:
        for l in f:
            sp = l.split('=')
            if len(sp) != 2:
                continue
            out[sp[0]] = sp[1].strip()

    return out


def main():
    """findmod detects "modularization" between two kernel configs.

    The intent here is to detect if our kernel config moves stuff into modules
    that isn't modularized in defconfig. The idea being deviating from
    defconfig unnecessarily (here modularizing things that are builtin in
    defconfig) should be avoided without good reason.
    """
    if len(sys.argv) != 3:
        print('expecting exactly 2 arguments', file=sys.stderr)
        sys.exit(1)

    a = load(sys.argv[1])
    b = load(sys.argv[2])
    # detect instances where a is 'y' while b is 'n' or 'm'
    for k, v in a.items():
        if k not in b or v not in ['y', 'm']:
            continue
        vb = b[k]
        if (v == 'y' and vb in ['m', 'n']) or (v == 'm' and vb == 'n'):
            print('{}: {} => {}'.format(k, v, vb))


if __name__ == '__main__':
    main()
