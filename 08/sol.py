#!/bin/env python3

from collections import deque

FILENAME="data"

# part one
frequencies=dict()
size=(0,0)

with open(FILENAME) as f:
    y = 0
    for l in f:
        x = 0
        for c in l.strip():
            if c != '.':
                frequencies.setdefault(c, deque())
                frequencies[c].append((x,y))
            x += 1
        y += 1
    size = (x,y)

def get_antinodes(ant_a, ant_b, size):
    def inbound(pos, size):
        (pos_x, pos_y) = pos
        (size_x, size_y) = size
        return pos_x >= 0 and pos_x < size_x and pos_y >= 0 and pos_y < size_y

    (ant_a_x, ant_a_y) = ant_a
    (ant_b_x, ant_b_y) = ant_b
    ant_diff_x = ant_a_x - ant_b_x
    ant_diff_y = ant_a_y - ant_b_y
    antinode_1 = (ant_a_x + ant_diff_x, ant_a_y + ant_diff_y)
    antinode_2 = (ant_b_x - ant_diff_x, ant_b_y - ant_diff_y)
    res = []
    if inbound(antinode_1, size):
        res.append(antinode_1)
    if inbound(antinode_2, size):
        res.append(antinode_2)
    return res

antinodes = set()
for f in frequencies:
    antennas = frequencies[f]
    while antennas:
        a = antennas.pop()
        for b in antennas:
            antinodes.update(get_antinodes(a,b, size))

print(len(antinodes))

# part two
frequencies=dict()
size=(0,0)

with open(FILENAME) as f:
    y = 0
    for l in f:
        x = 0
        for c in l.strip():
            if c != '.':
                frequencies.setdefault(c, deque())
                frequencies[c].append((x,y))
            x += 1
        y += 1
    size = (x,y)

def get_antinodes(ant_a, ant_b, size):
    def inbound(pos, size):
        (pos_x, pos_y) = pos
        (size_x, size_y) = size
        return pos_x >= 0 and pos_x < size_x and pos_y >= 0 and pos_y < size_y

    (ant_a_x, ant_a_y) = ant_a
    (ant_b_x, ant_b_y) = ant_b
    ant_diff_x = ant_a_x - ant_b_x
    ant_diff_y = ant_a_y - ant_b_y
    res = []
    # Go b->a direction
    next_antinode = (ant_b_x + ant_diff_x, ant_b_y + ant_diff_y)
    while inbound(next_antinode, size):
        res.append(next_antinode)
        next_antinode = (next_antinode[0] + ant_diff_x, next_antinode[1] + ant_diff_y)
    # bo a->b direction
    next_antinode = (ant_a_x - ant_diff_x, ant_a_y - ant_diff_y)
    while inbound(next_antinode, size):
        res.append(next_antinode)
        next_antinode = (next_antinode[0] - ant_diff_x, next_antinode[1] - ant_diff_y)
    return res

antinodes = set()
for f in frequencies:
    antennas = frequencies[f]
    while antennas:
        a = antennas.pop()
        for b in antennas:
            antinodes.update(get_antinodes(a,b, size))

print(len(antinodes))