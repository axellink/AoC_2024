#!/bin/env python3

import sys

ITERATIONS = 2000

def compute_secret(secret):
    tmp = secret * 64
    secret = secret ^ tmp
    secret = secret % 16777216

    tmp = secret // 32
    secret = secret ^ tmp
    secret = secret % 16777216

    tmp = secret * 2048
    secret = secret ^ tmp
    secret = secret % 16777216

    return secret

res = 0
with open(sys.argv[1]) as f:
    for l in f:
        init_secret = int(l.strip())
        secret = init_secret
        for _ in range(ITERATIONS):
            secret = compute_secret(secret)
        res += secret
print(res)