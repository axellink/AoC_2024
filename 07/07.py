#!/bin/env python3

FILENAME="07.txt"
datas = []
with open(FILENAME,'r') as f:
    for l in f:
        column = l.strip().split(":")
        data = [int(column[0])]
        data.append([int(i) for i in column[1].strip().split()])
        datas.append(data)


# First part
# I thought I was clever using binary, but part two got me ...
def process_one_data(data):
    result = data[0]
    nums = data[1]
    equals = False
    for i in range(2**(len(nums)-1)):
        res = nums[0] + nums[1] if i&1 else nums[0] * nums[1]
        for j in range(2,len(nums)):
            res = res + nums[j] if i&(1<<(j-1)) else res * nums[j]
        equals = res == result
        if equals:
            break
    return result if equals else 0

print(sum(process_one_data(i) for i in datas))

def two_op_calc(l, r, opcode):
    if opcode == 0:
        return int(str(l) + str(r))
    if opcode == 1:
        return l*r
    if opcode == 2:
        return l+r
    raise ValueError

def process_one_data_concat(data):
    result = data[0]
    nums = data[1]
    equals = False
    max = int("3"*(len(nums)-1))
    print(f"Calculating for {result}:{nums} with max = {max}")
    i = 0
    while i <= max:
        res = two_op_calc(nums[0], nums[1], i%10)
        for j in range(2,len(nums)):
            res = two_op_calc(res, nums[j], (i//(10**(j-1)))%10)
        equals = res == result
        if equals:
            break
        i += 1
        for j in range(len(nums)-1):
            cur_digit = (i//10**j)%10
            if cur_digit >= 3:
                i -= cur_digit*10**j
                i += 10**(j+1)
    return result if equals else 0

print(sum(process_one_data_concat(i) for i in datas))