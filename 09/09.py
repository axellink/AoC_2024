#!/bin/env python3
from collections import deque

with open("09.txt", 'r') as f:
    data = f.read().strip()

file_deq = deque()
void_space = []
is_file = True
file_id = 0

for c in data:
    if is_file:
        file_deq.extend([file_id]*int(c))
        file_id += 1
    else:
        void_space.append(int(c))
    is_file = not is_file

disk = []
file_id = 0
filling = False
void = void_space[file_id]
while file_deq:
    if not filling and file_deq[0] == file_id:
        disk.append(file_deq.popleft())
    elif not filling:
        filling = True
        void = void_space[file_id]
        file_id += 1
    elif filling and void > 0:
        disk.append(file_deq.pop())
        void -= 1
    else:
        filling = False

print(sum(k*v for (k,v) in enumerate(disk)))

def blocks_to_disk(blocks):
    res = []
    for (fid, size) in blocks:
        if size == 0:
            continue
        if fid is None:
            fid = 0
        res.extend([fid]*size)
    return res

blocks = []
is_file = True
file_id = 0
for c in data:
    fid = None
    size = int(c)
    if is_file:
        fid = file_id
        file_id += 1
    blocks.append((fid, size))
    is_file = not is_file

i=1
while blocks[-i][0] is None or blocks[-i][0] != 0:
    (fid, size) = blocks[-i]
    if fid is None:
        i += 1
    else:
        inserted = False
        for j in range(len(blocks)-i):
            (bid, bsize) = blocks[j]
            if bid is None and bsize >= size:
                blocks[j] = (bid, bsize-size)
                blocks.insert(j, (fid,size))
                blocks[-i] = (None, size)
                inserted = True
                break
        if not inserted:
            i += 1

print(sum(k*v for (k,v) in enumerate(blocks_to_disk(blocks))))