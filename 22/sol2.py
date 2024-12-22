#!/bin/env python3

import sys

ITERATIONS = 2000

SEQ_BANANAS = dict()

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
        secret = int(l.strip())
        price = secret % 10
        diff_seq = []
        curr_seq_bananas = dict()
        for _ in range(ITERATIONS):
            new_secret = compute_secret(secret)
            new_price = new_secret % 10
            diff_seq.append(new_price - price)
            if len(diff_seq) >= 4:
                tpl = tuple(diff_seq[-4:])
                if tpl not in curr_seq_bananas:
                    curr_seq_bananas[tpl] = new_price
            secret = new_secret
            price = new_price
        for k,v in curr_seq_bananas.items():
            SEQ_BANANAS.setdefault(k, 0)
            SEQ_BANANAS[k] += v
val = list(SEQ_BANANAS.values())
keys = list(SEQ_BANANAS.keys())
max_key = keys[val.index(max(val))]
print(max_key)
print(max(SEQ_BANANAS.values()))