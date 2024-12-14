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

final_pos = dict()
for r in swarm:
    fin = r.pos_after(100, size)
    final_pos.setdefault(fin,0)
    final_pos[fin] += 1

quadrants = [0]*4
for k,v in final_pos.items():
    def choose_quadrant(pos):
        (x,y) = pos
        (mid_x, mid_y) = (size[0]//2, size[1]//2)
        if x<mid_x and y<mid_y:
            return 0
        if x>mid_x and y<mid_y:
            return 1
        if x<mid_x and y>mid_y:
            return 2
        if x>mid_x and y>mid_y:
            return 3
        return None
    
    if (q := choose_quadrant(k)) is not None:
        quadrants[q] += v

print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])