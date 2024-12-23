#!/bin/env python3

import sys
import networkx as nx
import matplotlib.pyplot as plt

CO_GRAPH = nx.Graph()

with open(sys.argv[1]) as f:
    for l in f:
        (cpu1, cpu2) = l.strip().split('-')
        CO_GRAPH.add_edge(cpu1, cpu2)

t_cpu = [i for i in CO_GRAPH.nodes]
res = []
for c in t_cpu:
    res += list(nx.find_cliques(CO_GRAPH, [c]))
print(','.join(sorted(max(res, key=len))))