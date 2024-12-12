#!/bin/env python3

FILENAME = "data"
start_pos=[]

class Map:
    def __init__(self, map_array):
        self._size = (len(map_array[0]), len(map_array))
        self._map = map_array

    def get(self, pos):
        (size_x, size_y) = self._size
        (x, y) = pos
        if x < 0 or y < 0 or x >= size_x or y >= size_y:
            return -1
        else:
            return self._map[y][x]
    
    def get_size(self):
        return self._size
    
    def __str__(self):
        return '\n'.join(str(i) for i in self._map)

map_array = []
with open(FILENAME, 'r') as f:
    y = 0
    for l in f:
        map_array.append([])
        x = 0
        for c in l.strip():
            e = int(c)
            map_array[y].append(e)
            if e == 0:
                start_pos.append((x, y))
            x += 1
        y += 1

mmap = Map(map_array)

def hike(mmap, pos, expected_level):
    curr_level = mmap.get(pos)
    if curr_level != expected_level:
        return set()
    if curr_level == 9:
        return set([pos])
    diff_pos = [(1,0), (0,1), (-1,0), (0,-1)]
    res = set()
    for diff in diff_pos:
        res |= hike(mmap, (pos[0] + diff[0], pos[1] + diff[1]), curr_level+1)
    return res

print(sum(len(hike(mmap, pos, 0)) for pos in start_pos))


def hike2(mmap, pos, expected_level):
    curr_level = mmap.get(pos)
    if curr_level != expected_level:
        return 0
    if curr_level == 9:
        return 1
    diff_pos = [(1,0), (0,1), (-1,0), (0,-1)]
    res = 0
    for diff in diff_pos:
        res += hike2(mmap, (pos[0] + diff[0], pos[1] + diff[1]), curr_level+1)
    return res

print(sum(hike2(mmap, pos, 0) for pos in start_pos))