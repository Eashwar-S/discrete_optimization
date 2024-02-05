#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import time
Item = namedtuple("Item", ['index', 'value', 'weight'])

# Change Log:
# Version 1.1:
# 2024-04-02 - TODO Solve the knapsack problem using Dynamic Programming.
# 2024-04-02 - Improved "brach_and_bound" method by tightening the bounds using "bounding" function.
# 2024-04-02 - Implemented "brach_and_bound" method to solve the knapsack problem.
# 2024-02-02 - Implemented the greedy approach to solve the knapsack problem.

class Node:
    def __init__(self, index, item_index, item_selected, value, room, estimate, parent):
        self.index = index                  # Node index specifying the depth of branching
        self.item_index = item_index        # Item index in list of items
        self.item_selected = item_selected  #  Whether current node represents an included or excluded item
        self.value = value                  # Item current value
        self.room = room                    # Remaining capacity
        self.estimate = estimate            # Optimistic estimate of objective function value
        self.parent = parent                # For backtracking

def backtracking(node, n):
    decision_variables = [0]*n
    while node.parent is not None:
        if node.item_selected:
            decision_variables[node.item_index] = 1
        node = node.parent
    return decision_variables

def bounding(items, value, index, room):
    if room < 0:
        return 0
    else:
        j = index
        bound = value
        
        while j < len(items) and items[j].weight <= room:
            bound += items[j].value
            room -= items[j].weight
            j += 1
        
        if j < len(items):
            bound += room * (items[j].value / items[j].weight)
    
    return bound

def branch_and_bound(items, capacity, max_value):
    max_obj = -1
    root_node = Node(-1, -1, False, 0, capacity, max_value, None)
    last_explored_node = root_node
    node_list = []                                    # Stack for DFS
    node_list.append(root_node)
    start = time.time()
    while node_list and time.time() - start  < 120:   # Timeout after 120 seconds
        node = node_list.pop()
        
        if node.index + 1 < len(items):
            
            right_child_node = Node(index = node.index + 1,
                            item_index = items[node.index + 1].index, 
                            item_selected = False,
                            value = node.value,
                            room = node.room,
                            # estimate = node.estimate - items[node.index + 1].value,           # This method of bounding is not tight
                            estimate = bounding(items, node.value, node.index + 1, node.room),
                            parent = node)
            
            # Check if this child node is worth branching/exploring
            if right_child_node.estimate > max_obj:
                node_list.append(right_child_node)
                if max_obj < right_child_node.value:
                    max_obj = right_child_node.value
                    last_explored_node = right_child_node
            
            left_child_node = Node(index = node.index + 1,
                            item_index = items[node.index + 1].index,
                            item_selected = True,
                            value = node.value + items[node.index + 1].value,
                            room = node.room - items[node.index + 1].weight,
                            #estimate = node.estimate,
                            estimate = bounding(items, node.value + items[node.index + 1].value, node.index + 1, node.room - items[node.index + 1].weight),
                            parent = node)
            
            if left_child_node.estimate > max_obj:
                node_list.append(left_child_node)
                if max_obj < left_child_node.value:
                    max_obj = left_child_node.value
                    last_explored_node = left_child_node

    return max_obj, backtracking(last_explored_node, len(items))


def dp():
    pass

def solve_it(input_data):
    
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
        # max_value += int(parts[0])

    value = 0
    
    # greedy algorithm
    sorted_items = sorted(items, key=lambda x: x.value/x.weight,  reverse=True)
    
    max_value = 0
    cap = 0
    ind = -1
    for i, item in enumerate(sorted_items):
        if cap + item.weight <= capacity:
            max_value += item.value
            cap += item.weight
            ind = i

    if ind + 1 < len(items):
        max_value += (capacity - cap) * items[ind + 1].value / items[ind + 1].weight

    # Exact Approach - always finds the optimal solution wihout the timelimit condition in line 51
    value, taken = branch_and_bound(sorted_items,  capacity, max_value)
    
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

