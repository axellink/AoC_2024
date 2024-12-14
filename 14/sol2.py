#!/bin/env python3

FILENAME="data"

class Robot:
    def __init__(self, line):
        pos_line, v_line = line.split()
        self.pos = [int(i) for i in pos_line.split('=')[1].split(',')]
        self.v = [int(i) for i in v_line.split('=')[1].split(',')]

    def __str__(self):
        return f"Init pos : {self.pos}, velocity: {self.v}"
    
    def pos_after(self, n, size):
        (x,y) = self.pos
        (vx,vy) = self.v
        (sx,sy) = size
        return (
            (x+n*vx) % sx,
            (y+n*vy) % sy
        )

swarm = []
with open(FILENAME) as f:
    size = [int(i) for i in f.readline().strip().split()]
    for l in f:
        swarm.append(Robot(l.strip()))

def final_pos(n, size, swarm):
    final_pos = dict()
    for r in swarm:
        fin = r.pos_after(n, size)
        final_pos.setdefault(fin,0)
        final_pos[fin] += 1
    return final_pos

def print_map(size, pos):
    """
    the line detected is a little hack so I don't have to search through each seconds display
    """
    line = 0
    line_detected = False
    for y in range(size[1]):
        for x in range(size[0]):
            c = '#' if (x,y) in pos else '.'
            if c == '#':
                line += 1
            else :
                line = 0
            if line == 20:
                line_detected = True
            print(c, end='')
        print()
    return line_detected

n=0
while True:
    line_detected = print_map(size, final_pos(n, size, swarm))
    print(n, ' ', '-'*40)
    if line_detected:
        input()
    n+=1