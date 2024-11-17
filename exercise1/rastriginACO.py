#!/usr/bin/python3
from antsys import AntWorld
from antsys import AntSystem
import numpy as np
import random

from rastriginUtils import rastrigin
from evalUtils import c_optimize

TOO_BIG = 1000000

def main():
    train_ants()
    

def train_ants(old=True, verbose=True, n=5):
    # parameters
    interval_values = 13

    num_ants = 100
    max_iterations = 200
    early_stop_after_same_it = 50
    pheromone_weight = .5

    interval = np.hstack([np.linspace(-5.12, 0, num=interval_values), np.linspace(0, 5.12, num=interval_values)[1:]])
    # generate nodes for the graph
    # node = (id, dim, value)
    nodes_old = []
    for dim in range(1, n+1):
        for i, value in enumerate(interval):
            node = (i+dim*(interval_values*2-1), dim, value)
            nodes_old.append(node)
    random.shuffle(nodes_old)

    #new way of generating nodes --> bad, since does not allow to pick same node for multiple x_i!
    #node = (id, value)
    nodes = []
    for i, value in enumerate(interval):
        node = (i, value)
        nodes.append(node)
    random.shuffle(nodes)

    # The world (new_world) is created from the nodes as a either a cyclic or a complete graph.
    if old:
        # new_world = AntWorld(nodes_old, rastrigin_rules_old, lambda path: rastrigin_cost_old(path, n), lambda path, candidate: rastrigin_heuristic_old(path, candidate, n), true, 10)
        new_world = AntWorld(nodes_old, 
                             rastrigin_rules_old, 
                             lambda path: rastrigin_cost_old(path, n), 
                             lambda path, candidate: rastrigin_heuristic2_old(path, candidate, n), 
                             False, 10)
    else:
        # new_world = AntWorld(nodes, lambda start, end: rastrigin_rules(start, end, n), lambda path: rastrigin_cost(path, n), lambda path, candidate: rastrigin_heuristic(path, candidate, n), True, 10)
        new_world = AntWorld(nodes, 
                             lambda start, end: rastrigin_rules(start, end, n), 
                             lambda path: rastrigin_cost(path, n), 
                             lambda path, candidate: rastrigin_heuristic2(path, candidate, n), 
                             True, 10)

    # Configure ant_opt as an AntSystem.
    ant_opt = AntSystem(world=new_world,
                        n_ants=num_ants,
                        alpha=pheromone_weight
                        )

    # Execute the optimization loop.
    iterations = c_optimize(ant_opt,
                            max_iterations,
                            early_stop_after_same_it,
                            verbose=verbose
                            )

    # for iteration in iterations:
    #     print(iteration)
                
    # Show details about the best solution found.
    if old:
        print_solution_old(ant_opt.g_best[2], n)
    else:
        print_solution(ant_opt.g_best[2], n)

    return iterations


# we can either choose the end node as value for the function (0) or not (1)
def rastrigin_rules_old(start, end):
    return [0, 1]

def rastrigin_rules(start, end, n):
    return [i for i in range(n+1)]

# used to calculate the cost of a path
def rastrigin_cost_old(path, n):
    mask = np.array([0 for i in range(n)])
    # mask = np.array([False for i in range(n)])
    x = [0 for i in range(n)]
    for edge in path:
        if edge.info == 1:
            # set x value and note that an x value was chosen for this position
            x[edge.end[1]-1] = edge.end[2]
            mask[edge.end[1]-1] = mask[edge.end[1]-1] + 1
    if (mask != 1).any():
        # not all values set or one value set more than once
            return TOO_BIG
    #         if mask[edge.end[1]-1]:
    #             # we have already chosen a value and do not want two competing ones
    #             return TOO_BIG
    #         else:
    #             mask[edge.end[1]-1] = True
    #             x[edge.end[1]-1] = edge.end[2]
    # if sum(mask) < len(mask):
    #     # not all values set
    #         return TOO_BIG
    return rastrigin(x)

def rastrigin_cost(path, n):
    mask = np.array([0 for i in range(n)])
    x = [0 for i in range(n)]
    for edge in path:
        if edge.info > 0:
            # set x value and note that an x value was chosen for this position
            x[edge.info-1] = edge.end[1]
            mask[edge.info-1] = mask[edge.info-1] + 1
    if (mask != 1).any():
        # not all values set or one value set more than once
            return TOO_BIG
    return rastrigin(x)

# ants prefere to include values that have not been set already
def rastrigin_heuristic_old(path, candidate, n):
    mask = np.array([False for i in range(n)])
    # x = [0 for i in range(n)]
    for edge in path:
        if edge.info == 1:
            mask[edge.end[1]-1] = True
    if candidate.info == 1 and not mask[candidate.end[1]-1]:
        return 0
    elif candidate.info == 0:
        return 1
    else:
        return 2

# ants look at the rastrigin function with the candidate
def rastrigin_heuristic2_old(path, candidate, n):
    mask = np.array([False for i in range(n)])
    x = np.random.sample(n) * 10 - 5
    for edge in path:
        if edge.info == 1:
            mask[edge.end[1]-1] = True
            x[edge.end[1]-1] = edge.end[2]
    if candidate.info == 1 and not mask[candidate.end[1]-1]:
        x[candidate.end[1]-1] = candidate.end[2]
        return rastrigin(x) # use our candidate
    elif candidate.info == 0:
        return rastrigin(x) # just use the random variables
    else:
        return TOO_BIG
    
def rastrigin_heuristic(path, candidate, n):
    mask = np.array([False for i in range(n)])
    for edge in path:
        if edge.info > 0:
            mask[edge.info-1] = True
    if candidate.info > 0 and not mask[candidate.info-1]:
        return 0
    elif candidate.info == 0:
        return 1
    else:
        return 2
    
def rastrigin_heuristic2(path, candidate, n):
    mask = np.array([False for i in range(n)])
    x = np.random.sample(n) * 10 - 5
    # x = [0 for i in range(n)] #TODO: a different heuristic could try rastrigin w/ randomly initialized x, with set x_i and the candidate changed
    for edge in path:
        if edge.info > 0:
            mask[edge.info-1] = True
            x[edge.info-1] = edge.end[1]
    if candidate.info > 0 and not mask[candidate.info-1]:
        x[candidate.info-1] = candidate.end[1]
        return rastrigin(x)
    elif candidate.info == 0:
        return rastrigin(x)
    else:
        return TOO_BIG

# no preference for one path over another 
def simple_rastrigin_heuristic(path, candidate):
    return 1

# for displaying the found solution
def print_solution_old(path, n):
    print('chosen nodes:')
    print('| id | i| value|')

    x = [0 for i in range(n)]
    for edge in path:
        if(edge.info == 1):
            print('|%4i|%g|%g|' % edge.end)
            x[edge.end[1]-1] = edge.end[2]

    if rastrigin_cost_old(path, n) == TOO_BIG:
        print('no valid solution found')
    else:
        print('rastgirin(x) = %g' % rastrigin(x))

def print_solution(path, n):
    print('chosen nodes:')
    print('| id | i| value|')

    x = [0 for i in range(n)]
    for edge in path:
        if(edge.info > 0):
            print('|%4i|%g|%g|' % (edge.end[0], edge.info, edge.end[1]))
            x[edge.info-1] = edge.end[1]
            
    if rastrigin_cost(path, n) == TOO_BIG:
        print('no valid solution found')
    else:
        print('rastgirin(x) = %g' % rastrigin(x))
    
# def solution_from_path(path, n):
#     x = [0 for i in range(n)]
#     for edge in path:
#         if(edge.info > 0):
#             x[edge.info-1] = edge.end[1]
#     return x

def solution_from_path_old(path, n):
    x = [0 for i in range(n)]
    for edge in path:
        if(edge.info == 1):
            x[edge.end[1]-1] = edge.end[2]
    return x



if __name__ == '__main__':
    main()