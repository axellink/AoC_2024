#!/usr/bin/env python3

import copy
import os

"""
That shit works !
it takes time, but it works
also never expect python to handle out of bound well with negative
a_list[-3] is valid !
yeah I knew it, still I got my ass handed to me
"""

#FILENAME = "test"
FILENAME = "data"
orig_map = []
with open(FILENAME, 'r') as f:
    orig_map = []
    for l in f:
        orig_map.append(list(l.strip()))


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, pos):
        return Position(self.x + pos.x, self.y + pos.y)

    def __eq__(self, pos):
        if not pos:
            return False
        return self.x == pos.x and self.y == pos.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

class Move:
    MOVE = [Position(0,-1),
            Position(1,0),
            Position(0,1),
            Position(-1,0)
    ]
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __eq__(self, move):
        return self.pos == move.pos and self.direction == move.direction

    def next(self, map):
        front_pos = self.front_pos(map)
        if not map.is_inbound(front_pos):
            raise IndexError
        if map.is_obstacle(front_pos):
            return Move(self.pos, (self.direction+1)%4)
        return Move(front_pos, self.direction)
    
    def front_pos(self, map):
        return self.pos + self.MOVE[self.direction]

class Map:
    def __init__(self, map):
        self._map = copy.deepcopy(map)
        self._x = len(self._map[0])
        self._y = len(self._map)
        for x in range(self._x):
            for y in range(self._y):
                cur_pos = Position(x,y)
                if self.get(cur_pos) == '^':
                    self._orig_pos = cur_pos
                    self.mark_pos(cur_pos)
    
    def __str__(self):
        return f"{self._x} columns, {self._y} rows\n" + '\n'.join(' '.join(i) for i in self._map)

    def get_size(self):
            return (self._x, self._y)

    def get(self, pos):
        return self._map[pos.y][pos.x]

    def mark_pos(self, pos):
        if pos != self._orig_pos:
            self._map[pos.y][pos.x] = "X"

    def is_inbound(self, pos):
        return pos.x >= 0 and pos.y >=0 and pos.x < self._x and pos.y < self._y

    def is_obstacle(self, pos):
        return self.get(pos) == "#" or self.get(pos) == "O"

    def get_orig_pos(self):
        return self._orig_pos

    def count_marked(self):
        return sum(sum(e == "X" or e =="^" for e in row) for row in self._map)

    def add_obstacle(self, pos):
        self._map[pos.y][pos.x] = "O"
    

class Guard:
    def __init__(self, map, ghost=False):
        self._map = map
        self._move = Move(map.get_orig_pos(), 0)
        self._move_history = {}
        self._looping = False
        self._looping_if = set()
        self._ghost = ghost

    def _would_be_looping(self):
        """
        see if the guard would loop if there was an hypothetical obstacle in front 
        """
        front_pos = self._move.front_pos(self._map)
        if self._map.is_obstacle(front_pos) or front_pos in self._looping_if:
            return
        ghost_map = Map(orig_map)
        ghost_map.add_obstacle(front_pos)
        ghost = Guard(ghost_map, True)
        ghost.run()
        if ghost.is_looping():
            self._looping_if.add(front_pos)

    def _record_move(self):
        self._move_history.setdefault(self._move.pos, [])
        self._move_history[self._move.pos].append(self._move.direction)

    def move(self):
        self._map.mark_pos(self._move.pos)
        if not self._ghost:
            self._would_be_looping()
        if self._move.pos in self._move_history and self._move.direction in self._move_history[self._move.pos]:
            self._looping = True
        self._record_move()
        self._move = self._move.next(self._map)
    
    def run(self):
        while True:
            try:
                self.move()
                if self.is_looping():
                    break
            except IndexError:
                break
            except:
                raise

    def __str__(self):
        return f"Guard at {self._move.pos}"

    def get_history(self):
        return self._move_history

    def is_looping(self):
        return self._looping
    
    def looping_obstacles(self):
        return self._looping_if

map = Map(orig_map)
#print(map)
guard = Guard(map)
guard.run()
print(map.count_marked())
print(len(guard.looping_obstacles()))