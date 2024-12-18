#!/bin/env python3

import sys
import functools
import math
import heapq
from collections import deque

DIRS = [
    (1,0), # RIGHT
    (0,1), # DOWN
    (-1,0), # LEFT
    (0,-1) # UP
]

def add_pos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

@functools.total_ordering
class Pos:
    def __init__(self, pos, parent=None, distance=math.inf):
        self.pos = pos
        self.parent = parent
        self.distance = distance
    
    def __hash__(self):
        return hash(self.pos)
    
    def __eq__(self, n):
        return hash(self) == hash(n)
    
    def __lt__(self, n):
        return self.pos < n.pos
    
    def __str__(self):
        return f"{self.pos}"

class Map:
    def __init__(self, filename):
        with open(filename) as f:
            (size_x, size_y, n_bytes) = f.readline().strip().split(',')
            self.size = (int(size_x), int(size_y))
            row = ['.'] * self.size[0]
            self.map = [row.copy() for i in range(self.size[1])]
            for i in range(int(n_bytes)):
                (x,y) = f.readline().strip().split(',')
                self.map[int(y)][int(x)] = "#"
                self.last_byte_pushed = (int(x), int(y))
            self.next_bytes = deque()
            for l in f:
                (x,y) = l.strip().split(',')
                self.next_bytes.append((int(x), int(y)))
            self.final_pos = (self.size[0]-1, self.size[1]-1)
        
    def __str__(self):
        return '\n'.join(''.join(i) for i in self.map)
    
    def _inbound(self, pos):
        (x,y)=pos
        return x>=0 and y>=0 and x<self.size[0] and y<self.size[1]

    def get(self, pos):
        return self._inbound(pos) and self.map[pos[1]][pos[0]] == "."

    def print_visited(self, visited):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if (x,y) in visited:
                    print('O', end='')
                else:
                    print(self.map[y][x], end='')
            print()

    def pushdown_byte(self):
        self.last_byte_pushed = self.next_bytes.popleft()
        (x,y) = self.last_byte_pushed
        self.map[y][x] = "#"



# LET'S GO DIJKSTRA
def find_shortest(map, final_pos):
    visited = dict()
    pq = [(0,Pos((0,0), distance = 0))]
    while pq:
        dist, pos = heapq.heappop(pq)
        if pos.pos == final_pos:
            path = []
            while pos:
                path.append(pos)
                pos = pos.parent
            return path[::-1]

        adj_pos = [Pos(add_pos(pos.pos, i), pos, pos.distance+1) for i in DIRS]
        for p in adj_pos:
            if map.get(p.pos):
                if p.pos in visited:
                    old_pos = visited[p.pos]
                    if p.distance < old_pos.distance:
                        old_pos.distance = p.distance
                        old_pos.parent = p.parent
                        heapq.heappush(pq,(old_pos.distance, old_pos))
                else:
                    visited[p.pos] = p
                    heapq.heappush(pq, (p.distance, p))

mmap = Map(sys.argv[1])

i = 0
while path := find_shortest(mmap, mmap.final_pos):
    print(i)
    mmap.pushdown_byte()
    i+=1
print(mmap.last_byte_pushed)