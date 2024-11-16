#!/usr/bin/python3
from antsys import AntWorld
from antsys import AntSystem
import numpy as np
import random

from rastriginUtils import rastrigin
from evalUtils import c_optimize

# parameters        
n = 5
interval_values = 10

num_ants = 100
max_iterations = 100
early_stop_after_same_it = 20
pheromone_weight = .5

# generate nodes for the graph
interval = np.hstack([np.linspace(-5.12, 0, num=interval_values), np.linspace(0, 5.12, num=interval_values)[1:]])
nodes = []
nodes_old = []
for dim in range(1, n+1):
    for i, value in enumerate(interval):
        node = (i+dim*(interval_values*2-1), dim, value)
        nodes_old.append(node)

#new way of generating nodes
for i, value in enumerate(interval):
    node = (i, value)
    nodes.append(node)


random.shuffle(nodes)

# we can either choose the end node as value for the function (0) or not (1)
def rastrigin_rules_old(start, end):
    return [0, 1]

def rastrigin_rules(start, end):
    return [i for i in range(n+1)]

# used to calculate the cost of a path
def rastrigin_cost_old(path):
    mask = np.array([False for i in range(n)])
    x = [0 for i in range(n)]
    for edge in path:
        if edge.info == 1:
            if mask[edge.end[1]-1]:
                # we have already chosen a value and do not want two competing ones
                return 1000000
            else:
                mask[edge.end[1]-1] = True
                x[edge.end[1]-1] = edge.end[2]
    if sum(mask) < len(mask):
        # not all values set
            return 1000000
    return rastrigin(x)

def rastrigin_cost(path):
    # mask = np.zeros(n)
    mask = np.array([0 for i in range(n)])
    x = [0 for i in range(n)]
    for edge in path:
        if edge.info > 0:
            x[edge.info-1] = edge.end[1]
            mask[edge.info-1] = mask[edge.info-1] + 1
            # if mask[edge.end[1]-1]:
            #     # we have already chosen a value and do not want two competing ones
            #     return 1000000
            # else:
            #     mask[edge.end[1]-1] = True
            #     x[edge.end[1]-1] = edge.end[2]
    if (mask != 1).any():
    # if sum(mask) < len(mask):
        # not all values set
            return 1000000
    return rastrigin(x)

# ants prefere to include values that have not been set already
def rastrigin_heuristic_old(path, candidate):
    mask = np.array([False for i in range(n)])
    x = [0 for i in range(n)]
    for edge in path:
        if edge.info == 1:
            mask[edge.end[1]-1] = True
    if candidate.info == 1 and not mask[candidate.end[1]-1]:
        return 0
    elif candidate.info == 0:
        return 1
    else:
        return 2
    
def rastrigin_heuristic(path, candidate):
    mask = np.array([False for i in range(n)])
    # x = [0 for i in range(n)] #TODO: a different heuristic could try rastrigin w/ randomly initialized x, with set x_i and the candidate changed
    for edge in path:
        if edge.info > 0:
            mask[edge.info-1] = True
    if candidate.info > 0 and not mask[candidate.info-1]:
        return 0
    elif candidate.info == 0:
        return 1
    else:
        return 2

# no preference for one path over another 
def simple_rastrigin_heuristic(path, candidate):
    return 1

# for displaying the found solution
def print_solution_old(path):
    print('chosen nodes:')
    print('| id | i| value|')

    x = [0 for i in range(n)]
    # mask = np.array([False for i in range(n)])
    for edge in path:
        if(edge.info == 1):
            print('|%4i|%g|%g|' % edge.end)
            x[edge.end[1]-1] = edge.end[2]
            # mask[edge.end[1]-1] = True
            
    if rastrigin_cost(path) == 1000000:
        print('no valid solution found')
        return
    print('rastgirin(x) = %g' % rastrigin(x))

def print_solution(path):
    print('chosen nodes:')
    print('| id | i| value|')

    x = [0 for i in range(n)]
    # mask = np.array([False for i in range(n)])
    for edge in path:
        if(edge.info > 0):
            print('|%4i|%g|%g|' % (edge.end[0], edge.info, edge.end[1]))
            x[edge.info-1] = edge.end[1]
            # mask[edge.end[1]-1] = True
            
    if rastrigin_cost(path) == 1000000:
        print('no valid solution found')
        return
    print('rastgirin(x) = %g' % rastrigin(x))
    
def solution_from_path(path):
    x = [0 for i in range(n)]
    for edge in path:
        if(edge.info > 0):
            x[edge.info-1] = edge.end[1]
    return x

# The world (new_world) is created from the nodes as a either a cyclic or a complete graph.
# new_world = AntWorld(nodes, rastrigin_rules, rastrigin_cost, rastrigin_heuristic, False, 10)
# new_world = AntWorld(nodes_old, rastrigin_rules_old, rastrigin_cost_old, rastrigin_heuristic_old, False, 10)
new_world = AntWorld(nodes, rastrigin_rules, rastrigin_cost, rastrigin_heuristic, True, 10)

# # Configure ant_opt as an AntSystem.
ant_opt = AntSystem(world=new_world, n_ants=num_ants, alpha=pheromone_weight)

# # Execute the optimization loop.

iterations = c_optimize(ant_opt, max_iterations,early_stop_after_same_it)
for iteration in iterations:
    print(iteration)

# # Show details about the best solution found.
print_solution(ant_opt.g_best[2])
