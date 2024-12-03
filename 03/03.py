#!/bin/env python3

import re

# Loading data
with open("03.txt") as f:
    memory = f.read().replace("\n","")

# first part
r = re.compile("mul\((\d{1,3}),(\d{1,3})\)")
print(sum(int(i[0])*int(i[1]) for i in r.findall(memory)))

# second part

# This attempt with regex gives too much mul, so a too high answer, which the function does not give
# I don't now why and will investigate
#filter_r = re.compile("don't\(\).*?do\(\)")
#filtered_mem = filter_r.sub("",memory)
#print(sum(int(i[0])*int(i[1]) for i in r.findall(filtered_mem)))

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
                break
        if not enabled: # look for the next do()
            if m := do_re.search(memory,index):
                index = m.end()
                enabled = True
            else: # no match left, end of file
                break
    return res

print(sum(int(i[0])*int(i[1]) for i in get_mult_filtered(memory)))
