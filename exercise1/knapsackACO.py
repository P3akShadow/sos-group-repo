#!/usr/bin/python3
from antsys import AntWorld
from antsys import AntSystem
import numpy as np
import random

import knapsackUtils as ks #TODO: unused

# parameters        
num_knapsacks = 3
min_capacity = 100
max_capacity = 500

num_items = 100
min_weight = 10
max_weight = 100
min_value = 60
max_value = 4000

num_ants = 100
max_iterations = 100
early_stop_after_same_it = 20


# generate and show knapsack capacity
knapsacks = [random.randint(min_capacity,max_capacity) for i in range(num_knapsacks)]
print('knapsack capacities: ' if len(knapsacks) > 1 else 'knapsack capacity: ', knapsacks)

# generate and show available items
print('\navailable items:')
print('|item|weight| value|')
items = []
for i in range(num_items):
    #TODO: we might want non-int values for at least the weight
    items.append((i, random.randint(min_weight,max_weight), random.randint(min_value,max_value)))
    print('|%4i|%6i|%6i|' % items[i])
  

# we can either not put the item in a knapsack (0) or put it in one of the n knapsacks (i)
def knapsack_rules(start, end):
    return [i for i in range(num_knapsacks+1)]

# used to calculate the cost of a path
def knapsack_cost(path):
    k_values = [0 for i in range(num_knapsacks)]
    k_weights = [0 for i in range(num_knapsacks)]
    for edge in path:
        if edge.info != 0:
            k_values[edge.info-1] += edge.end[2]
            k_weights[edge.info-1] += edge.end[1]
        
    cost = 1/sum(k_values)
    for i, knapsack_capacity in enumerate(knapsacks):
        if k_weights[i] > knapsack_capacity:
            # one of the knapsacks is over capacity
            cost += 1
    for edge in path:
        if edge.info == 0 and edge.end[1] <= max([knapsacks[i]-k_weights[i] for i in range(num_knapsacks)]):
            # the item would still fit in at least one of the knapsacks
            cost += 1
    return cost
    

# ants prefere to chose paths such that items get put into knapsacks with leftover capacity
def knapsack_heuristic(path, candidate):
    # k_values = [0 for i in range(num_knapsacks)]
    k_weights = [0 for i in range(num_knapsacks)]
    for edge in path:
        if edge.info != 0:
            # k_values[edge.info-1] += edge.end[2]
            k_weights[edge.info-1] += edge.end[1]
    if candidate.info == 0:
        return 1
    if k_weights[candidate.info-1]+candidate.end[1] <= knapsacks[candidate.info-1]:
        # if the knapsack still has capacity for the item, return a low number, maybe percentage of capacity remaining
        # return 0
        return k_weights[candidate.info-1]/knapsacks[candidate.info-1]
    else:
        return 2

# no preference for one path over another 
def simple_knapsack_heuristic(path, candidate):
    return 1

# for displaying the found solution
def print_solution(path):
    for i, knapsack_capacity in enumerate(knapsacks):
        print('chosen items for knapsack %d:' % (i+1))
        print('| id |weight| value|')
        k_value = 0
        k_weight = 0

        for edge in path:
            if(edge.info == i+1):
                print('|%4i|%6i|%6i|' % edge.end)
                k_value += edge.end[2]
                k_weight += edge.end[1]

        print('weight: %g out of capacity: %g\nvalue = %g' % (k_weight, knapsack_capacity, k_value))

# The world (new_world) is created from the items as a either a cyclic or a complete graph.
random.shuffle(items) # shuffling input data is good practice in general
new_world_cyclic = AntWorld(items, knapsack_rules, knapsack_cost, knapsack_heuristic, False)
# new_world_connected = AntWorld(items, knapsack_rules, knapsack_cost, knapsack_heuristic, True, 10)

# # Configure ant_opt as an AntSystem.
ant_opt_cyclic = AntSystem(world=new_world_cyclic, n_ants=num_ants)
# ant_opt_connected = AntSystem(world=new_world_connected, n_ants=num_ants)

# # Execute the optimization loop.
ant_opt_cyclic.optimize(max_iterations,early_stop_after_same_it)
# ant_opt_connected.optimize(max_iterations,early_stop_after_same_it)

# # Show details about the best solution found.
print_solution(ant_opt_cyclic.g_best[2])
# print_solution(ant_opt_connected.g_best[2])
