#!/bin/env python3

DIRS = {
    '^': (0,-1),
    '>': (1,0),
    'v': (0,1),
    '<': (-1,0)
}

def add_pos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

wh_map = []
wh_map_size = (0,0)
moves = []
r_pos = (0,0)
with open("data") as f:
    y = 0
    while l := f.readline().strip():
        row = []
        x = 0
        for i in list(l):
            row.append(i)
            if i =="@":
                r_pos = (x,y)
            x += 1
        wh_map.append(row)
        y += 1
    wh_map_size = (x, y)
    while l := f.readline().strip():
        moves += list(l)

def get(pos):
    return wh_map[pos[1]][pos[0]]

def set(pos, c):
    wh_map[pos[1]][pos[0]] = c

def move_object(old_pos, new_pos):
    curr_c = get(old_pos)
    set(old_pos, '.')
    set(new_pos, curr_c)

def print_map():
    for y in range(wh_map_size[1]):
        for x in range(wh_map_size[0]):
            print(wh_map[y][x], end='')
        print()

print_map()
print(wh_map_size)
print(r_pos)

def move(pos, dir):
    curr_c = get(pos)
    front_pos = add_pos(pos, dir)
    front_c = get(front_pos)
    if front_c == '#':
        return pos
    if front_c == '.' or move(front_pos, dir) != front_pos:
        move_object(pos, front_pos)
        return front_pos
    return pos
    

for m in moves:
    r_pos = move(r_pos,DIRS[m])

def gps_sum():
    res = 0
    for x in range(wh_map_size[0]):
        for y in range(wh_map_size[1]):
            if get((x,y)) == 'O':
                res += x + 100*y
    return res

print_map()
print(gps_sum())