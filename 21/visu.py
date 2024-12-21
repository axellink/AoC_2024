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

def move_robot(pos, touch):
    match touch:
        case "^": return (pos[0], pos[1]-1)
        case "v": return (pos[0], pos[1]+1)
        case ">": return (pos[0]+1, pos[1])
        case "<": return (pos[0]-1, pos[1])

def activate(robot, robots_pos, robot_seq):
    if robot == 0:
        robot_seq[0] += RDIGI[robots_pos[robot]]
        return RDIGI[robots_pos[robot]]
    else:
        touch = RDPAD[robots_pos[robot]]
        robot_seq[robot] += touch
        if touch == "A":
            return activate(robot - 1, robots_pos, robot_seq)
        else:
            for j in range(robot):
                robot_seq[j] += "."
            robots_pos[robot-1] = move_robot(robots_pos[robot - 1], touch)
            return ""

def verify(robot, sequence):
    robots_pos = [DIGI["A"]] + [DPAD["A"]] * (robot -1)
    robot_seq = [""] * (robot+1)
    res = ""
    for i in sequence:
        robot_seq[robot] += i
        if i == "A":
            res += activate(robot-1, robots_pos, robot_seq)
        else:
            for j in range(robot):
                robot_seq[j] += "."
            robots_pos[robot-1] = move_robot(robots_pos[robot-1], i)
    return res, robot_seq



def find_shortest_digpad(pad, code, curr_pos, seq = ""):
    if code == "":
        return [seq]
    if curr_pos not in pad.values():
        return []
    target_pos = pad[code[0]]
    if curr_pos == target_pos:
        return find_shortest_digpad(pad, code[1:], curr_pos, seq + "A")
    (curr_x, curr_y) = curr_pos
    (target_x, target_y) = target_pos
    (dx, dy) = (target_x - curr_x, target_y - curr_y)
    res = []
    if dx > 0:
        res += find_shortest_digpad(pad, code, (curr_x + 1, curr_y), seq + ">")
    elif dx < 0:
        res += find_shortest_digpad(pad, code, (curr_x - 1, curr_y), seq + "<")
    if dy > 0:
        res += find_shortest_digpad(pad, code, (curr_x, curr_y + 1), seq + "v")
    elif dy < 0:
        res += find_shortest_digpad(pad, code, (curr_x, curr_y - 1), seq + "^")
    return res

codes = []

with open(sys.argv[1], 'r') as f:
    for l in f:
        codes.append(l.strip())

res = 0
for c in codes:
    value = int(c[:-1])

    shortests = find_shortest_digpad(DIGI, c, DIGI["A"])
    short_len = len(min(shortests, key=len))
    shortests = [i for i in shortests if len(i) == short_len]
    
    for r in range(2):
        new_shortests = []
        for i in shortests:
            new_shortests += find_shortest_digpad(DPAD, i, DPAD["A"])
        short_len = len(min(new_shortests, key=len))
        shortests = [i for i in new_shortests if len(i) == short_len]

short = shortests[0]
(code, seq) = verify(3, short)
print(code)
print('\n'.join([' '.join(list(i)).replace('.', ' ') for i in seq[::-1]]))
