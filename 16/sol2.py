#!/bin/env python3

import math
import sys
import functools

import heapq

#sys.setrecursionlimit(100000)
DIRS = [
    (1,0), # RIGHT
    (0,1), # DOWN
    (-1,0), # LEFT
    (0,-1) # UP
]

def add_pos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

@functools.total_ordering
class Node:
    def __init__(self, pos, dir, parent=[], distance=math.inf):
        self.pos = pos
        self.dir = dir
        self.parent = parent
        self.distance = distance
    
    def __hash__(self):
        return hash((self.pos[0], self.pos[1], self.dir))
    
    def __eq__(self, n):
        return hash(self) == hash(n)
    
    def __lt__(self, n):
        return (self.pos[0], self.pos[1], self.dir) < (n.pos[0], n.pos[1], n.dir)
    
    def __str__(self):
        return f"{self.pos} : {self.dir}"

class Map:
    def __init__(self, filename):
        self._map = []
        with open(filename, 'r') as f:
            y = 0
            for l in f:
                if 'S' in l:
                    self.start_pos=(l.index('S'), y)
                self._map.append(list(l.strip()))
                y += 1
        self._size = (len(self._map[0]), len(self._map))
    
    def __str__(self):
        return str(self._size) + '\n' + '\n'.join(''.join(i) for i in self._map)
    
    def get(self, pos):
        (x,y) = pos
        return self._map[y][x]

maze = Map(sys.argv[1])
print(maze)
print(maze.start_pos)

visited = dict()

def print_maze_visited():
    for y in range(maze._size[1]):
        for x in range(maze._size[0]):
            if any(((x,y),i) in visited for i in range(4)):
                print('X',end='')
            else:
                print(maze.get((x,y)), end = '')
        print()

# LET'S GO DIJKSTRA
def find_shortest():
    pq = [(0,Node(maze.start_pos, 0, distance = 0))]
    while pq:
        dist, node = heapq.heappop(pq)
        if maze.get(node.pos) == 'E':
            return node

        adj_node = [
            Node(add_pos(node.pos, DIRS[node.dir]), node.dir, [node], node.distance + 1),
            Node(node.pos, (node.dir+1)%4, [node], node.distance + 1000),
            Node(node.pos, (node.dir-1)%4, [node], node.distance + 1000)
        ]
        for n in adj_node:
            if maze.get(n.pos) in '.ES':
                if (n.pos,n.dir) in visited:
                    old_node = visited[(n.pos, n.dir)]
                    if n.distance == old_node.distance:
                        old_node.parent += n.parent
                    if n.distance < old_node.distance:
                        old_node.distance = n.distance
                        old_node.parent = n.parent
                        heapq.heappush(pq,(old_node.distance, old_node))
                else:
                    visited[(n.pos, n.dir)] = n
                    heapq.heappush(pq, (n.distance, n))

last_node_on_shortest = find_shortest()
best_seat = set()
def get_best_seat(node):
    best_seat.add(node.pos)
    if node.parent:
        for n in node.parent:
            get_best_seat(n)
get_best_seat(last_node_on_shortest)

def print_best_seat():
    for y in range(maze._size[1]):
        for x in range(maze._size[0]):
            if (x,y) in best_seat:
                print('X',end='')
            else:
                print(maze.get((x,y)), end = '')
        print()

print_best_seat()
print(len(best_seat))