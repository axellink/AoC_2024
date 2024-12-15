#!/bin/env python3

import os
import time

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
            if i == '.' or i =='#':
                row += [i,i]
            elif i == 'O':
                row += ['[',']']
            else:
                row += ['@', '.']
                r_pos = (x,y)
            x += 2
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

def can_move_to_h(pos, dir):
    curr_c = get(pos)
    if curr_c == '.':
        return True
    elif curr_c == "#":
        return False
    else:
        return can_move_to_h(add_pos(pos, dir), dir)   

def can_move_to_v(pos, dir):
    curr_c = get(pos)
    if curr_c == '.':
        return True
    if curr_c == '#':
        return False
    if curr_c == '[':
        poses = [add_pos(pos,dir), add_pos(add_pos(pos, DIRS['>']),dir)] 
    else:
        poses = [add_pos(add_pos(pos, DIRS['<']),dir), add_pos(pos,dir)]
    return all([can_move_to_v(pos, dir) for pos in poses])

def move_h(pos, dir):
    front_pos = add_pos(pos,dir)
    front_c = get(front_pos)
    if front_c == '#':
        raise Exception("MOVING INTO WALLS")
    if front_c == '.':
        move_object(pos, front_pos)
        return front_pos
    move_h(front_pos, dir)
    move_object(pos,front_pos)
    return front_pos

def move_v(pos, dir):
    curr_c = get(pos)
    if curr_c == '@':
        poses = [pos]
    elif curr_c == '[':
        poses = [pos, add_pos(pos, DIRS['>'])] 
    else:
        poses = [add_pos(pos, DIRS['<']), pos] 
    for _pos in poses:
        front_pos = add_pos(_pos, dir)
        front_c = get(front_pos)
        if front_c == '#':
            raise Exception(f"MOVING INTO WALLS {_pos} {front_pos}")
        if front_c == '.':
            move_object(_pos, front_pos)
        else:
            move_v(front_pos, dir)
            move_object(_pos, front_pos)
    return add_pos(pos, dir)

def move(pos, dir_c):
    dir = DIRS[dir_c]
    if dir_c in '^v':
        if can_move_to_v(add_pos(pos, dir), dir):
            return move_v(pos, dir)
        else:
            return pos
    else:
        if can_move_to_h(add_pos(pos, dir), dir):
            return move_h(pos, dir)
        else:
            return pos

for m in moves:
    r_pos = move(r_pos,m)

def gps_sum():
    res = 0
    for x in range(wh_map_size[0]):
        for y in range(wh_map_size[1]):
            if get((x,y)) == '[':
                res += x + 100*y
    return res

print_map()
print(gps_sum())