#!/bin/env python3

rules = {}
orders = []

with open("05.txt",'r') as f:
    for l in f:
        if '|' in l:
            data = l.strip().split('|')
            rules.setdefault(data[0],[])
            rules[data[0]].append(data[1])
        elif ',' in l:
            orders.append(l.strip().split(','))

# first part
def is_good_order(order, rules):
    is_good_order = True
    for i in range(len(order)):
        if (order[i] in rules) and (any(e in order[:i] for e in rules[order[i]])):
            is_good_order = False
            break
    return is_good_order

good_orders = []
bad_orders = [] # for second part
for order in orders:
    if is_good_order(order, rules):
        good_orders.append(order)
    else:
        bad_orders.append(order)

print(sum(int(o[len(o)//2]) for o in good_orders)) # 4569

# second part
def please_order(order, rules):
    """
    The idea here is, for every page in a line, get every indexes of a page before that should be after
    Once we have those indexes (if there is some), swap the current page with the first page found
    Doing this we ensure that all the rules concerning the current page are respected
    We do so until the order is good

    I'm pretty sure this would be also doable with a sorting algorithm and a good comp function
    Might try it later
    """
    while not is_good_order(order, rules):
        for i in range(len(order)):
            pos_before = []
            if (page := order[i]) in rules: # Check we have a rule on this page before
                for p in rules[page]:
                    try:
                        pos_before.append(order[:i].index(p))
                    except ValueError:
                        pass
            if pos_before:
                new_place = min(pos_before)
                order[new_place], order[i] = order[i], order[new_place]


for order in bad_orders:
    please_order(order, rules)

print(sum(int(o[len(o)//2]) for o in bad_orders)) # 6456