#!/usr/bin/python3
from antsys import AntWorld
from antsys import AntSystem
import numpy as np
import random

import knapsackUtils as ks

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


# generate and show knapsack capacity; simple knapsack problem
# knapsacks = [random.randint(min_capacity,max_capacity) for i in range(num_knapsacks)]
# knapsacks = [random.randint(min_capacity,max_capacity) for i in range(1)]
# print('knapsack capacities: ' if len(knapsacks) > 1 else 'knapsack capacity: ', knapsacks)

# show available items
# print('\navailable items:')
# print('|item|weight| value|')
# items = []
# for i in range(num_items):
    #TODO: we might want non-int values for at least the weight
    # items.append((i, random.randint(min_weight,max_weight), random.randint(min_value,max_value)))
    # print('|%4i|%6i|%6i|' % items[i])

# generate and show items + knapsack, adjustable    
knapsacks, items = ks.generateInstance(num_knapsacks, num_items)
knapsacks_cap_array = np.array(knapsacks)
# print(knapsacks_cap_array)
dim = items.shape[1] - 1
items_as_nodes = []
for i, item in enumerate(items):
    l = [i]
    l.extend(item)
    items_as_nodes.append(tuple(l))

random.shuffle(items_as_nodes) # shuffling input data is good practice in general

# we can either not put the item in a knapsack (0) or put it in one of the n knapsacks (i)
def knapsack_rules(start, end):
    return [i for i in range(num_knapsacks+1)]

# used to calculate the cost of a path
def knapsack_cost(path):
    k_values = [0 for i in range(num_knapsacks)]
    # k_weights = np.array([[0 for j in range(dim)] for i in range(num_knapsacks)])
    k_weights = np.zeros(knapsacks_cap_array.shape)
    for edge in path:
        if edge.info != 0:
            k_values[edge.info-1] += edge.end[1]
            for i in range(dim):
                k_weights[edge.info-1][i] += edge.end[2+i]
        
    cost = 1/sum(k_values)
    if not (np.array(knapsacks) >= k_weights).all():
        # one of the knapsacks is over capacity
        cost += 1 
    for edge in path:
        # if edge.info == 0 and np.array(edge.end[2:]) <= max([knapsacks[i]-k_weights[i] for i in range(num_knapsacks)]): 
        if edge.info == 0 and (np.array(edge.end[2:]) <= knapsacks_cap_array-k_weights).all(1).any():
            # the item would still fit in at least one of the knapsacks
            cost += 1
    return cost
    

# ants prefere to chose paths such that items get put into knapsacks with leftover capacity
def knapsack_heuristic(path, candidate):
    k_weights = np.zeros(knapsacks_cap_array.shape)
    for edge in path:
        if edge.info != 0:
            for i in range(dim):
                k_weights[edge.info-1][i] += edge.end[2+i]

    if candidate.info == 0:
        return 1
    if (k_weights[candidate.info-1]+ np.array(candidate.end[2:]) <= knapsacks_cap_array[candidate.info-1]).all(): #TODO
        # if the knapsack still has capacity for the item, return a low number, maybe percentage of capacity remaining
        return 0
        # np.max(k_weights[candidate.info-1]/np.array(knapsacks[candidate.info-1]))
    else:
        return 2

# no preference for one path over another 
def simple_knapsack_heuristic(path, candidate):
    return 1

# for displaying the found solution
def print_solution(path): #TODO
    total_value = 0.
    for i, knapsack_capacity in enumerate(knapsacks):
        print(knapsack_capacity)
        print('chosen items for knapsack %d:' % (i+1))
        s = '| id | value|' + "".join(["  dim" +str(i+1)+"|" for i in range(dim)])
        # print('| id |weight| value|')  #TODO
        print(s)
        k_value = 0
        k_values = np.array([0. for i in range(num_knapsacks)])
        k_weights = np.zeros(np.array(knapsack_capacity).shape)

        for edge in path:
            if(edge.info == i+1):
                s = "|" + "|".join([str(np.round(value, 3)) for value in edge.end]) + "|"
                print(s) #TODO 
                # print('|%4i|%6i|%6i|' % edge.end) #TODO 
                k_value += edge.end[1]
                for j in range(dim):
                    k_weights[j] = k_weights[j] + edge.end[2+j]
        print("value = %g" % k_value)
        used_capacity = np.prod(k_weights)
        available_capacity = np.prod(knapsack_capacity)
        if used_capacity > available_capacity:
            print("Knapsack over capacity!")
        else:
            print("%g out of capacity was %g used\n" % (used_capacity, available_capacity))
        total_value += k_value
        # print('weight: %g out of capacity: %g\nvalue = %g' % (k_weights, knapsack_capacity, k_value))
    print("total value stored: %g" % total_value)

# The world (new_world) is created from the items as a either a cyclic or a complete graph.
new_world = AntWorld(items_as_nodes, knapsack_rules, knapsack_cost, knapsack_heuristic, False)
# new_world= AntWorld(items, knapsack_rules, knapsack_cost, knapsack_heuristic, True, 10)

# # Configure ant_opt as an AntSystem.
ant_opt = AntSystem(world=new_world, n_ants=num_ants)

# # Execute the optimization loop.
ant_opt.optimize(max_iterations, early_stop_after_same_it)

# # Show details about the best solution found.
print_solution(ant_opt.g_best[2])
