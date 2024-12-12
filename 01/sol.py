#!/bin/env python3

from collections import Counter

l1 = []
l2 = []

# Loading data
with open("data") as f:
	while line := f.readline()[:-1]:
		[e1, e2] = line.split("   ")
		l1.append(int(e1))
		l2.append(int(e2))

l1.sort()
l2.sort()

# first part
print(sum(abs(i-j) for (i,j) in zip(l1, l2)))

# second part
counter = Counter(l2)
print(sum(i*counter[i] for i in l1))
