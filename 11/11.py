#!/bin/env python3

MAX_BLINK = 75
CACHE = dict()
with open("data") as f:
    init = [int(i) for i in f.readline().strip().split()]

def naive(stone, blink=0):
    if (stone, blink) in CACHE:
        return CACHE[(stone, blink)]
    res = 0
    if blink == MAX_BLINK:
        res = 1
    else:
        s = str(stone)
        if len(s)%2 == 0:
            m = len(s)//2
            res = naive(int(s[:m]), blink+1) + naive(int(s[m:]), blink+1)
        else:
            res = naive(1, blink+1) if stone == 0 else naive(stone*2024, blink+1)
    CACHE[(stone, blink)] = res
    return res

print(sum(naive(i) for i in init))