#!/bin/env python3

import sys
from functools import cache

patterns = []
designs = []

with open(sys.argv[1]) as f:
    patterns = sorted(f.readline().strip().split(', '), key=len)[::-1]
    f.readline()
    for l in f:
        designs.append(l.strip())

#print(MAX_LENGTH)
#print(patterns_by_length)
#print(designs)

# OK SO for this one I have to admit that after hours attempting a lot of thing
# I went to see some solutions
# stumbled upon this one : https://github.com/janek37/advent-of-code/blob/main/2024/day19.py
# The difference is in the approach, while I try to push a pattern into the design
# this solution looks at what patterns could go for the beginning of the design
# and then recursively do the same on the remaining of the design
# this is way easier than my way of thinking ...

@cache
def search_design(design):
    if design == '':
        return 1
    res = 0
    for pattern in patterns:
        if design.startswith(pattern):
            res += search_design(design[len(pattern):])
    return res

print(sum(search_design(d) for d in designs))