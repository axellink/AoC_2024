#!/bin/env python3

reports = []

# Loading data
with open("02.txt") as f:
	while line := f.readline()[:-1]:
		reports.append([int(i) for i in line.split()])

# First part
def is_safe(report): 
    goes_up = report[0]<report[1]
    for i in range(0,len(report)-1):
        x = report[i]
        y = report[i+1]
        if goes_up and not (x<y and y<x+4):
            return 0
        elif not goes_up and not (x>y and y>x-4):
            return 0
    return 1

print(sum([is_safe(i) for i in reports]))

# Second part
def is_safe_dampener(report): 
    goes_up = report[0]<report[1]
    dampened = False
    for i in range(0,len(report)-1):
        x = report[i]
        y = report[i+1]
        if goes_up and not (x<y and y<x+4):
            if dampened:
                return 0
            else:
                dampened = True
        elif not goes_up and not (x>y and y>x-4):
            if dampened:
                return 0
            else:
                dampened = True
    return 1

print(sum([is_safe_dampener(i) for i in reports]))
