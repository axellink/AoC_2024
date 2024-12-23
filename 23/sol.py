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
                cpu = tcpu_links.setdefault(cpu1_name, [])
                cpu.append(cpu2_name)
            if cpu2_name[0] == 't':
                cpu = tcpu_links.setdefault(cpu2_name, [])
                cpu.append(cpu1_name)

triple_co = set()

for name, tcpu_link in tcpu_links.items():
    for i in tcpu_link:
        for j in tcpu_link:
            if i != j:
                if f"{i}-{j}" in links:
                    triple_co.add(','.join(sorted([name, i, j])))
print(len(triple_co))