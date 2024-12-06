#!/usr/bin/env python3

class Table:
    def __init__(self, filename):
        self._table = []
        self._x = 0
        self._y = 0
        with open(filename,'r') as f:
            for l in f:
                row = list(l.strip())
                self._table.append(row)
                self._x = len(row)
                self._y += 1
    
    def __str__(self):
        return f"{self._x} columns, {self._y} rows\n" + '\n'.join(' '.join(i) for i in self._table)

    def get_size(self):
            return (self._x, self._y)

    def get(self, x, y):
        return self._table[y][x]

    def _get_positions(self, base, dir, length):
        if dir == 0:
            return [base] * 4
        elif dir > 0:
            return [base + i for i in range(length)]
        else:
            return [base - i for i in range(length)]

    def get_one_direction(self, x, y, direction, length):
        (dir_x, dir_y) = direction
        pos_x = self._get_positions(x, dir_x, length)
        if any(i < 0 or i >= self._x for i in pos_x):
            return []
        pos_y = self._get_positions(y, dir_y, length)
        if any(i < 0 or i >= self._y for i in pos_y):
            return []
        return [self.get(e[0], e[1]) for e in zip(pos_x, pos_y)]

    def get_all_directions(self, x, y, length):
        return [self.get_one_direction(x, y, (i, j), length) 
                for i in range(-1,2) 
                for j in range(-1,2)]
    
t = Table("04.txt")
word = "XMAS"
res = 0
(x,y) = t.get_size()
for i in range(x):
    for j in range(y):
        res += sum("".join(e) == word 
                   for e in t.get_all_directions(i,j,len(word)))

print(res)

def get_cross(t, x, y, length):
    branch_1 = t.get_one_direction(x, y, (1,1), length)
    branch_2 = t.get_one_direction(x+2, y, (-1,1), length)
    return [branch_1, branch_1[::-1], branch_2, branch_2[::-1]]

word = "MAS"
res = 0
for i in range(x):
    for j in range(y):
        if sum("".join(e) == word for e in get_cross(t, i, j, len(word))) ==2 :
            res += 1
print(res)