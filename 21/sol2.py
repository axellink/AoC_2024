#!/bin/env python3

import sys

DIGI={
    "7": (0,0),
    "8": (1,0),
    "9": (2,0),
    "4": (0,1),
    "5": (1,1),
    "6": (2,1),
    "1": (0,2),
    "2": (1,2),
    "3": (2,2),
    "0": (1,3),
    "A": (2,3)
}

DPAD={
    "^": (1,0),
    "A": (2,0),
    "<": (0,1),
    "v": (1,1),
    ">": (2,1),
}

RDIGI = {v:k for k,v in DIGI.items()}
RDPAD = {v:k for k,v in DPAD.items()}

ALL_DPAD_PATH = [i+j for i in DPAD for j in DPAD]

def compute_path(pad, rpad, path, seq = ""):
    if path[0] == path[1]:
        return [seq]
    (curr_x, curr_y) = pad[path[0]]
    (target_x, target_y) = pad[path[1]]
    (dx, dy) = (target_x - curr_x, target_y - curr_y)
    res = []
    if dx > 0:
        next_pos = (curr_x + 1, curr_y)
        res += compute_path(pad, rpad, rpad[next_pos] + path[1], seq + ">") if next_pos in rpad else []
    elif dx < 0:
        next_pos = (curr_x - 1, curr_y)
        res += compute_path(pad, rpad, rpad[next_pos] + path[1], seq + "<") if next_pos in rpad else []
    if dy > 0:
        next_pos = (curr_x, curr_y + 1)
        res += compute_path(pad, rpad, rpad[next_pos] + path[1], seq + "v") if next_pos in rpad else []
    elif dy < 0:
        next_pos = (curr_x, curr_y - 1)
        res += compute_path(pad, rpad, rpad[next_pos] + path[1], seq + "^") if next_pos in rpad else []
    return res

ALL_DPAD_COMPUTED_PATH = {i:compute_path(DPAD, RDPAD, i) for i in ALL_DPAD_PATH}
costs = {k:1 for k in ALL_DPAD_PATH}


def compute_cost(path, costs):
    tmp = []
    for p in ALL_DPAD_COMPUTED_PATH[path]:
        prev = "A"
        res = 0
        for i in p:
            res += costs[prev + i]
            prev=i
        tmp.append(res + costs[prev + "A"])
    return min(tmp)

for _ in range(25):
    new_costs = {p:compute_cost(p, costs) for p in ALL_DPAD_PATH}
    costs = new_costs

codes = []

with open(sys.argv[1], 'r') as f:
    for l in f:
        codes.append(l.strip())

res = 0
for code in codes:
    prev = "A"
    code_res = 0
    for char in code:
        paths = compute_path(DIGI, RDIGI, prev+char)
        tmp = []
        for path in paths:
            above_prev = "A"
            above_res = 0
            for above_char in path:
                above_res += costs[above_prev + above_char]
                above_prev = above_char
            tmp.append(above_res + costs[above_prev + "A"])
        prev = char
        code_res += min(tmp)
    print(code_res)
    res += code_res * int(code[:-1])
print(res)