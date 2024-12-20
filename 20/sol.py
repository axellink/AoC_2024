#!/bin/env python3

import sys

DIRS = [
    (1,0), # RIGHT
    (0,1), # DOWN
    (-1,0), # LEFT
    (0,-1) # UP
]

SCORE_MIN = 100

def add_pos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

path = dict()
shortcuts = dict()

class Map:
    def __init__(self, filename):
        self._map = []
        with open(filename, 'r') as f:
            y = 0
            for l in f:
                if 'S' in l:
                    self.start_pos=(l.index('S'), y)
                if 'E' in l:
                    self.end_pos = (l.index('E'), y)
                self._map.append(list(l.strip()))
                y += 1
        self._size = (len(self._map[0]), len(self._map))
    
    def __str__(self):
        return str(self._size) + '\n' + '\n'.join(''.join(i) for i in self._map)
    
    def get(self, pos):
        (x,y) = pos
        try:
            return self._map[y][x] in "S.E"
        except IndexError:
            return False

class Pathnode:
    def __init__(self, map, from_pos, pos, score):
        self.pos = pos
        self.score = score
        self.end = map.end_pos == pos
        self.next_pos = None
        self.cheat_pos = set()
        if not self.end:
            for i in DIRS:
                next = add_pos(pos,i)
                if map.get(next) and next != from_pos:
                    self.next_pos = next
                elif next != from_pos:
                    for j in DIRS:
                        renext = add_pos(next,j)
                        if renext != pos and map.get(renext):
                            self.cheat_pos.add(renext)
    
    def __str__(self):
        return f"{self.pos} : {self.score} -> {self.next_pos} => {self.cheat_pos}"

mmap = Map(sys.argv[1])
curr_score = 0
curr_pos = mmap.start_pos
from_pos = None
while True:
    node = Pathnode(mmap, from_pos, curr_pos, curr_score)
    path[curr_pos] = node
    if node.end:
        break
    from_pos = curr_pos
    curr_pos = node.next_pos
    curr_score += 1

for pos, node in path.items():
    for c in node.cheat_pos:
        c_node = path[c]
        score = c_node.score - node.score - 2
        if score >= SCORE_MIN:
            entry = shortcuts.setdefault(score, [])
            entry.append((c_node.pos, node.pos))

print(sum(len(sc_list) for score, sc_list in shortcuts.items()))