#!/bin/env python3

import pprint

DIRECTIONS={
    "u": (-1,0),
    "d": (1,0),
    "l": (0,-1),
    "r": (0,1)
}

class Map:
    def __init__(self, filename):
        self.map = []
        with open(filename, 'r') as f:
            for l in f:
                self.map.append(list(l.strip()))
        self.size = (len(self.map[0]), len(self.map))

    def __str__(self):
        return str(self.size) + '\n' + '\n'.join(' '.join(i) for i in self.map)

    def get(self, pos):
        (size_x, size_y) = self.size
        (x,y) = pos
        if x < 0 or y < 0 or x >= size_x or y >= size_y:
            return None
        else:
            return self.map[y][x]

class Plots:
    def __init__(self, pos, map):
        self.type = map.get(pos)
        self.pos = pos
        self.wall = []
        self.next = []
        for d, diff in DIRECTIONS.items():
            p = (self.pos[0] + diff[0], self.pos[1] + diff[1])
            if map.get(p) == self.type:
                self.next.append(p)
            else:
                self.wall.append(d)
    
    def fences(self):
        return 4 - len(self.next)
    
    def __str__(self):
        return f"{self.pos} : {self.type} -> {self.next}"
    
    def __hash__(self):
        return hash(self.pos)
    
    def __eq__(self, o):
        if isinstance(o, Plots):
            return self.pos == o.pos
        return False
    
class Region:
    def __init__(self, init_plot, map):
        self.plots = {init_plot.pos : init_plot} 
        self.pos_walled = {d:set() for d in DIRECTIONS}
        self._construct(init_plot, map)
    
    def _construct(self, plot, map):
        for d in DIRECTIONS:
            if d in plot.wall:
                self.pos_walled[d].add(plot.pos)
        for p in plot.next:
            if p not in self.plots:
                new = Plots(p, map)
                self.plots[p] = new
                self._construct(new, map)
    
    def __str__(self):
        return f"{self.plots[list(self.plots)[0]].type} : {len(self.plots)}"

    def contains_pos(self, pos):
        return pos in self.plots

    def fence_price(self):
        return sum(p.fences() for k,p in self.plots.items()) * len(self.plots)
    
    def optimized_price(self):
        return self.compute_sides() * len(self.plots)
    
    def compute_sides(self):
        def compute_segment_same_const(vars):
            res = 1
            for i in range(len(vars)-1):
                if vars[i]+1 != vars[i+1]:
                    res += 1
            return res
        
        sides = 0
        for d, pos in self.pos_walled.items():
            if d in ['u','d']:
                const_key = lambda pos:pos[0]
                var_key = lambda pos:pos[1]
            else:
                const_key = lambda pos:pos[1]
                var_key = lambda pos:pos[0]
            same_const = dict()
            for i in pos:
                const = const_key(i)
                entry = same_const.setdefault(const, [])
                entry.append(var_key(i))
            sides += sum(
                compute_segment_same_const(sorted(e))
                for const, e in same_const.items()
            )
        return sides


regions = []

m = Map("data")
(size_x, size_y) = m.size
for x in range(size_x):
    for y in range(size_y):
        if not any(r.contains_pos((x,y)) for r in regions):
            regions.append(Region(Plots((x,y), m), m))

print(sum(r.fence_price() for r in regions))
print(sum(r.optimized_price() for r in regions))