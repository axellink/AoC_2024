#!/bin/env python3

import time
import numpy

class Machine:
    def __init__(self, data_lines):
        def parse_button(button_line):
            return [
                int(i.strip().split('+')[1])
                for i in button_line.split(':')[1].split(',')
            ]
        
        self.ax, self.ay = parse_button(data_lines[0])
        self.bx, self.by = parse_button(data_lines[1])
        self.px, self.py = [
            int(i.strip().split('=')[1]) + 10000000000000
            for i in data_lines[2].split(':')[1].split(',')
        ]
        self.optimize()
    
    def __str__(self):
        return f"A: X+{self.ax}, Y+{self.ay}\nB: X+{self.bx}, Y+{self.by}\nP: X={self.px}, Y={self.py}"

    def optimize(self):
        """
        AND THEN I REMEMBER MATH EXISTS
        """

        def on_prize(a,b):
            return (a*self.ax + b*self.bx) == self.px and (a*self.ay + b*self.by) == self.py

        num_a = self.px * self.by - self.bx * self.py
        num_b = self.ax * self.py - self.ay * self.px
        denom = self.ax * self.by - self.ay * self.bx
        sol = (num_a // denom, num_b // denom)
        self.optim = sol if on_prize(sol[0], sol[1]) else None

    def get_cost(self):
        if self.optim:
            return 3*self.optim[0] + self.optim[1]
        return None

costs = []
with open("data", 'r') as f:
    blank = '\n'
    while blank == '\n':
        data_lines=[f.readline().strip(), f.readline().strip(), f.readline().strip()]
        blank = f.readline()
        costs.append(Machine(data_lines).get_cost())

print(costs.count(None))
print(sum(i for i in costs if i))