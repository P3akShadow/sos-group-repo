#!/usr/bin/python3

import numpy as np
from knapsackUtils import evaluate, generateInstance

from deap import base, creator, tools
import random

def main():
    train_GA()

def train_GA(verbose=True,knapsacks=10, items=100, iterations=100, dim=3):
    knapsackSizes = [[10],[10]]
    itemSizes = [[9],[7],[5],[4],[1]]
    #print(evaluate(knapsackSizes, itemSizes, range(5)))
    #print(evaluate(knapsackSizes, itemSizes, [0,4,2,1,3]))

    # knapsacks = 10
    # items = 200
    #(knapsackSizes, itemSizes) = generateInstance(knapsacks, items, knapsack_mean=10, items_mean=3, dimensions=dim)
    (knapsackSizes, itemSizes) = generateInstance(knapsacks, items, dimensions=dim)
    if verbose:
        print(knapsackSizes)
        print(itemSizes)
    #print(itemSizes)
    #print(evaluate(knapsackSizes, itemSizes, range(10)))

    creator.create("FitnessKnapsack", base.Fitness, weights=(10.0, -0.01))
    creator.create("Individual", list, fitness=creator.FitnessKnapsack)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(items), items)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)

    #pxPartialyMathed uses Partially Matched Crossover
    #This means: Exchange a random sequence in the middle
    #for each exchanged element
    #Create a mapping that maps elements to the element in the same position but on the other side
    #map the occuring elements accordingly to keep the permutation property
    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=2.1/items)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", lambda x: evaluate(knapsackSizes, itemSizes, x))

    result = optimize(toolbox, itemSizes, knapsackSizes, iterations=iterations, verbose=verbose)
    if verbose:
        print(result)

    return result


def optimize(toolbox, itemSizes, knapsackSizes, population=400, iterations=100, verbose=True):
    pop = [toolbox.individual() for _ in range(population)]
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    best_ind = tools.selTournament(pop, 1, tournsize=len(pop))[0]
    starting_fitness = best_ind.fitness.values
    
    best_ind
    bestFit = []
    globalBest = -float("inf")
    for g in range(iterations):
        if verbose:
            print("#################")
            print(f"generation {g}")
            print("#################")
        
        best_ind = tools.selTournament(pop, 1, tournsize=len(pop))[0]
        evaluate(knapsackSizes, itemSizes, best_ind, True)
        if verbose:
            print(best_ind)
            print(best_ind.fitness.values)
        if globalBest < best_ind.fitness.values[0]:
            globalBest = best_ind.fitness.values[0]
        bestFit += [(g, best_ind.fitness.values[0], globalBest)]
    
        offspring = toolbox.select(pop, len(pop))
        offspring = list(toolbox.map(toolbox.clone, offspring))
    
        for child1, child2 in zip(offspring[::2], offspring[1::2]):  #[x::2] takes every other element starting from x
            if random.random() < 0.8:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child1.fitness.values
    
        for mutant in offspring:
            if random.random() < 0.3:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        pop[:] = offspring
    
    if verbose:
        print(f"sum elements {np.sum(itemSizes)}")
        print(f"sum knapsacks {np.sum(knapsackSizes)}")
        print(f"starting fitness was {starting_fitness}")
        print(f"last best fitness {best_ind.fitness.values}")

    return bestFit

if __name__ == "__main__":
    main()
