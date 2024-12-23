#!/bin/env python3

import sys

tcpu_links = dict()
links = set()

with open(sys.argv[1]) as f:
    for l in f:
        link = l.strip()
        links.add(link)
        if 't' in link:
            (cpu1_name, cpu2_name) = link.split('-')
            if cpu1_name[0] == 't':
                cpu = tcpu_links.setdefault(cpu1_name, set())
                cpu.add(cpu2_name)
            if cpu2_name[0] == 't':
                cpu = tcpu_links.setdefault(cpu2_name, set())
                cpu.add(cpu1_name)

def find_largest(curr_set = set(), available = set(), deep=0):
    if len(available) == 0:
        return curr_set
    connected_to_curr_set = set([
        i for i in available
        if all([
            f"{i}-{j}" in links or f"{j}-{i}" in links
            for j in curr_set
        ])
    ])
    tmp = []
    for c in connected_to_curr_set:
        next_set = curr_set.copy()
        next_set.add(c)
        next_available = connected_to_curr_set.copy()
        next_available.remove(c)
        tmp.append(find_largest(next_set, next_available, deep +1))
    return max(tmp, key=len) if len(tmp) > 0 else set()

res = []
for name, tcpu_link in tcpu_links.items():
    print(name)
    tmp = []
    for c in tcpu_link:
        tmp.append(find_largest(set([name, c]), tcpu_link))
    res.append(max(tmp, key=len))
print(','.join(sorted(list(max(res, key=len)))))