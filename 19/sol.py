#!/bin/env python3

import sys
from functools import cache

MAX_LENGTH = 0
patterns_by_length = {}
designs = []

with open(sys.argv[1]) as f:
    patterns = f.readline().strip().split(', ')
    for p in patterns:
        length = len(p)
        entry = patterns_by_length.setdefault(length, [])
        entry.append(p)
    MAX_LENGTH = max(patterns_by_length)
    f.readline()
    for l in f:
        designs.append(l.strip())

#print(MAX_LENGTH)
#print(patterns_by_length)
#print(designs)

# This works, but to be honest with you, I'm not completely sure why it does ....
# I'm actually even pretty sure there would be some cases it should not work

@cache
def search_design(design, curr_len):
    #print(design, curr_len)
    if design == '':
        return True
    if curr_len == 0:
        return False
    res = False
    for p in patterns_by_length[curr_len]:
        if p in design:
            res = all([search_design(d, min(len(d), curr_len)) for d in design.split(p)])
            if res:
                return res
    if res:
        return res
    return search_design(design, curr_len-1)

print(sum(search_design(d, min(len(d), MAX_LENGTH)) for d in designs))