#!/usr/bin/python3
from antsys import AntWorld
from antsys import AntSystem
import numpy as np
import random

from tspUtils import generateInstance, evaluate

# parameters        
num_cities = 20
gridsize = 100

num_ants = 100
max_iterations = 100
early_stop_after_same_it = 50

# generate nodes for the graph
# interval = np.linspace(0.0, 5.12, num=interval_values)
nodes = []
# for dim in range(1, n+1):
    # for i, value in enumerate(interval):
        # node = (i+dim*interval_values, dim, value)
        # nodes.append(node)
for i in range(num_cities):
    nodes.append((i, random.randint(0,gridsize), random.randint(0,gridsize)))
    


# print(nodes)
# ID, x, y
# we add the euclidean distance to the nodes
def tsp_rules(start, end):
    return [(np.sqrt((start[1]-end[1])**2 + (start[2]-end[2])**2))] #TODO

# used to calculate the cost of a path, sum of the distances
def tsp_cost(path):
    result = 0
    for edge in path:
        result = result + edge.info
    return result

# ants prefere to include the closest node
def tsp_heuristic(path, candidate):
    return candidate.info #TODO prbly should penalize already included nodes - or not, seems to not do that anyways

# no preference for one path over another 
def simple_tsp_heuristic(path, candidate):
    return 1

# for displaying the found solution
def print_solution(path):
    # pass
    print('chosen nodes:')
    print('| id |    x |    y |')
    result = 0
    for edge in path:
        print('|%4i|%6i|%6i|' % edge.end)
        result = result + edge.info
    print('total path length = %g' % result)

# The world (new_world) is created from the nodes as a either a cyclic or a complete graph.
random.shuffle(nodes) # if we do not shuffle, cyclic immediately finds the shortest path due to the node distribution and the heuristic
#new_world_cyclic = AntWorld(nodes, tsp_rules, tsp_cost, tsp_heuristic, False)
new_world_connected = AntWorld(nodes, tsp_rules, tsp_cost, tsp_heuristic, True, 10)

# # Configure ant_opt as an AntSystem.
#ant_opt_cyclic = AntSystem(world=new_world_cyclic, n_ants=num_ants) # cyclic doesn't make any sense here
ant_opt_connected = AntSystem(world=new_world_connected, n_ants=num_ants)

# # Execute the optimization loop.
#ant_opt_cyclic.optimize(max_iterations,early_stop_after_same_it) # cyclic doesn't make any sense here
ant_opt_connected.optimize(max_iterations,early_stop_after_same_it)

# # Show details about the best solution found.
#print_solution(ant_opt_cyclic.g_best[2]) # cyclic doesn't make any sense here
print_solution(ant_opt_connected.g_best[2])
