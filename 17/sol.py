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

while True:
    try:
        opcode = program[i_p]
        op = program[i_p + 1]
        opcodes[opcode](op)
    except IndexError as e:
        print("Program halts with instruction pointer:", i_p)
        break
    except Exception as e:
        raise

print(','.join(str(i) for i in output))