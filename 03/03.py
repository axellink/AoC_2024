#!/bin/env python3

import re

# Loading data
with open("data") as f:
    memory = f.read().replace("\n","")

# first part
r = re.compile("mul\((\d{1,3}),(\d{1,3})\)")
print(sum(int(i[0])*int(i[1]) for i in r.findall(memory)))

# second part

# first option in regex removes don't()...do() blocks
# second option in regex removes a don't() to EOF block which has no do() in it
# the question mark in .*? makes the .* to be the shortest instead of the longest match
filtered_mem = re.sub("don't\(\).*?do\(\)|don't\(\).*$", "", memory)
print(sum(int(i[0])*int(i[1]) for i in r.findall(filtered_mem)))

# First, I forgot the case of a don't() with no matching do() until end of file
# so I made this function to be closer to the problem script
# you see with the prints in the function where I found my problem with the regex solution
def get_mult_filtered(memory):
    mul_or_dont_re = re.compile("mul\((\d{1,3}),(\d{1,3})\)|don't\(\)")
    do_re = re.compile("do\(\)")
    enabled = True
    res=[]
    index = 0
    while True:
        if enabled:
            if m := mul_or_dont_re.search(memory,index):
                index = m.end()
                values = m.group(1,2)
                if values == (None,None): # this is a don't()
                    enabled = False
                else: # this is a mult()
                    res.append(values)
            else: #no match left, end of file
                print("end of file while enabled")
                break
        if not enabled: # look for the next do()
            if m := do_re.search(memory,index):
                index = m.end()
                enabled = True
            else: # no match left, end of file
                print("end of file while disabled")
                break
    return res

print(sum(int(i[0])*int(i[1]) for i in get_mult_filtered(memory)))
