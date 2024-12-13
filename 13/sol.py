#!/bin/env python3

import time

class Machine:
    def __init__(self, data_lines):
        def parse_button(button_line):
            return [int(i.strip().split('+')[1]) for i in button_line.split(':')[1].split(',')]
        
        self.ax, self.ay = parse_button(data_lines[0])
        self.bx, self.by = parse_button(data_lines[1])
        self.px, self.py = [int(i.strip().split('=')[1]) for i in data_lines[2].split(':')[1].split(',')]
        print(self)
        start = time.time()
        self.optimize()
        print(time.time()-start)
    
    def __str__(self):
        return f"A: X+{self.ax}, Y+{self.ay}\nB: X+{self.bx}, Y+{self.by}\nP: X={self.px}, Y={self.py}"

    def optimize(self):
        # My idea will be to go with 0 A push and max B push to go beyond prize on either axis
        # Then while I'm not beyond, add A push, if i rego beyond remove B push
        # Do this until we either gain prize or we have max A push but not beyond prize anymore

        def beyond_prize(a,b):
            return (a*self.ax + b*self.bx) > self.px or (a*self.ay + b*self.by) > self.py

        def on_prize(a,b):
            return (a*self.ax + b*self.bx) == self.px and (a*self.ay + b*self.by) == self.py

        max_a = min(100, self.px // self.ax, self.py // self.ay)
        max_b = min(100, self.px // self.bx, self.py // self.by) 
        # Find first position with max B push
        a = 0
        b = max_b 
        while not on_prize(a,b):
            if beyond_prize(a,b):
                if b == 0:
                    if a > max_a:
                        self.optim = None
                        return
                    a -= 1
                else:
                    b -= 1
            else:
                if a > max_a:
                    self.optim = None
                    return
                a += 1
        self.optim = (a,b)

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