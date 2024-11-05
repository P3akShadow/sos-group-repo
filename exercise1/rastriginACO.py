#!/usr/bin/python3
from antsys import AntWorld
from antsys import AntSystem
import numpy as np
import random

from rastriginUtils import rastrigin

# parameters        
n = 5
interval_values = 10

num_ants = 100
max_iterations = 100
early_stop_after_same_it = 50

# generate nodes for the graph
interval = np.linspace(0.0, 5.12, num=interval_values)
nodes = []
for dim in range(1, n+1):
    for i, value in enumerate(interval):
        node = (i+dim*interval_values, dim, value)
        nodes.append(node)

# print(nodes)

# we can either choose the end node as value for the function (0) or not (1)
def rastrigin_rules(start, end):
    return [0, 1]

# used to calculate the cost of a path
def rastrigin_cost(path):
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

# ants prefere to include values that have not been set already
def rastrigin_heuristic(path, candidate):
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

# no preference for one path over another 
def simple_rastrigin_heuristic(path, candidate):
    return 1

# for displaying the found solution
def print_solution(path):
    print('chosen nodes:')
    print('| id | i| value|')

    x = [0 for i in range(n)]
    # mask = np.array([False for i in range(n)])
    for edge in path:
        if(edge.info == 1):
            print('|%4i|%2i|%6i|' % edge.end)
            x[edge.end[1]-1] = edge.end[2]
            # mask[edge.end[1]-1] = True
            
    if rastrigin_cost(path) == 1000000:
        print('no valid solution found')
        return
    print('rastgirin(x) = %g' % rastrigin(x))

# The world (new_world) is created from the nodes as a either a cyclic or a complete graph.
random.shuffle(nodes) # if we do not shuffle, cyclic immediately finds the shortest path due to the node distribution and the heuristic
new_world_cyclic = AntWorld(nodes, rastrigin_rules, rastrigin_cost, rastrigin_heuristic, False)
# new_world_connected = AntWorld(nodes, rastrigin_rules, rastrigin_cost, rastrigin_heuristic, True, 10)

# # Configure ant_opt as an AntSystem.
ant_opt_cyclic = AntSystem(world=new_world_cyclic, n_ants=num_ants)
# ant_opt_connected = AntSystem(world=new_world_connected, n_ants=num_ants)

# # Execute the optimization loop.
ant_opt_cyclic.optimize(max_iterations,early_stop_after_same_it)
# ant_opt_connected.optimize(max_iterations,early_stop_after_same_it)

# # Show details about the best solution found.
print_solution(ant_opt_cyclic.g_best[2])
# print_solution(ant_opt_connected.g_best[2])
