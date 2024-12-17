#!/bin/env python3

import sys

#make it pretty
A=0
B=1
C=2

reg = [0]*3
program = []
output = []
i_p = 0

def combo(operand):
    if operand == 7:
        raise ValueError("7 is reserved")
    if operand < 4:
        return operand
    return reg[operand - 4]

def adv(op):
    global i_p
    num = reg[A]
    den = 2**combo(op)
    reg[A] = num//den
    i_p += 2

def bxl(op):
    global i_p
    reg[B] = reg[B] ^ op
    i_p += 2

def bst(op):
    global i_p
    reg[B] = combo(op) % 8
    i_p += 2

def jnz(op):
    global i_p
    if reg[A] != 0:
        i_p = op
    else:
        i_p += 2

def bxc(op):
    global i_p
    reg[B] = reg[B] ^ reg[C]
    i_p += 2

def out(op):
    global i_p
    output.append(combo(op) % 8)
    i_p+=2

def bdv(op):
    global i_p
    num = reg[A]
    den = 2**combo(op)
    reg[B] = num//den
    i_p += 2
    
def cdv(op):
    global i_p
    num = reg[A]
    den = 2**combo(op)
    reg[C] = num//den
    i_p += 2
    
opcodes = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

with open(sys.argv[1], 'r') as f:
    for i in range(3):
        reg[i] = int(f.readline().split(':')[1].strip())
    f.readline()
    program = [int(i) for i in f.readline().split(':')[1].strip().split(',')]

def run_prog():
    global i_p
    i=0
    while True:
        try:
            opcode = program[i_p]
            op = program[i_p + 1]
            opcodes[opcode](op)
            i += 1
        except IndexError as e:
            #print("Program halts with instruction pointer:", i_p, "after ", i, "instructions")
            break
        except Exception as e:
            raise

def reset(i=0):
    global i_p
    global output
    global reg
    i_p = 0
    output = []
    reg = [i,0,0]

# Tried something with dichotomy, still too long (if it ever works btw)

def high_low(n_items):
    def range_max(start, n):
        half = start
        i = 0
        while half > 1:
            reset(i)
            run_prog()
            if len(output) >= n:
                i -= half
            else:
                i += half
            half = half // 2
        i -= 5
        reset(i)
        run_prog()
        while len(output) < n:
            i += 1
            reset()
            reg[A] = i
            run_prog()
        return i
    
    def large_max(n):
        i = 1
        reset(i)
        run_prog()
        while len(output) <= n:
            i *= 10
            reset(i)
            run_prog()
        return i
    
    max = large_max(n_items)
    print(max)
    return [
        range_max(max,n_items + 1) -1,
        range_max(max,n_items)
    ]

high, low = high_low(len(program))
print(low, high)

def list_blocks(low, high, nth, step):
    #print(low, high, nth, step)
    def large_max(low, high, nth, step, e):
        i = low
        reset(i)
        run_prog()
        while output[nth] == e and i < high:
            i += step
            reset(i)
            run_prog()
        return i if i < high else None
    
    def range_max(low, high, nth, e):
        i = low
        half = high-low
        while half > 1:
            #print("HALF", half)
            #print(i)
            reset(i)
            run_prog()
            #print("YOLO")
            #print(output[nth], e)
            if output[nth] == e:
                i += half
            else:
                i -= half
            half = half // 2
        i -= 5
        reset(i)
        run_prog()
        while output[nth] == e:
            i += 1
            reset(i)
            run_prog()
        return i
    
    res = []
    reset(low)
    run_prog()
    e = output[nth]
    max = large_max(low, high, nth, step, e)
    old_low = low
    while max:
        new_low = range_max(old_low, max, nth, e)
        res.append((e, [old_low, new_low-1]))
        reset(new_low)
        run_prog()
        e = output[nth]
        max = large_max(new_low, high, nth, step, e)
        old_low = new_low
    res.append((e,[old_low, high]))
    return res

print(list_blocks(low, high, 15, (high-low)//10))

def search(low, high, nth):
    e = program[nth]
    print("SEARCH:",low, high, nth, e, (high-low)//10)
    if nth <= 5:
        for i in range(low, high + 1):
            reset(i)
            run_prog()
            if output == program:
                return i
        return None
    blocks = [r[1] for r in list_blocks(low, high, nth, (high-low)//10)]
    for b in blocks:
        res = search(b[0], b[1], nth-1)
    if res:
        return res
    return None

print(search(low, high, len(program)-1))