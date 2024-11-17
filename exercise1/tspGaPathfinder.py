#!/usr/bin/python3

import numpy as np
from tspUtils import *
from deap import base, creator, tools
import random

def main():
    train_GA()

def train_GA(verbose=True, cities=50, iterations=300):
    instance = generateInstance(cities)
    if verbose:
        print(instance)

    creator.create("FitnessTsp", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessTsp)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(cities), cities)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)

    #pxPartialyMathed uses Partially Matched Crossover
    #This means: Exchange a random sequence in the middle
    #for each exchanged element
    #Create a mapping that maps elements to the element in the same position but on the other side
    #map the occuring elements accordingly to keep the permutation property
    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.03)
    toolbox.register("select", tools.selTournament, tournsize=4)
    toolbox.register("evaluate", lambda x: (evaluate(instance, x),))

    result = optimize(toolbox, population=4000, iterations=iterations, verbose=verbose)
    if verbose:
        print(result)

    return result


def optimize(toolbox, population=400, iterations=100, verbose=True):
    pop = [toolbox.individual() for _ in range(population)]
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    best_ind = tools.selTournament(pop, 1, tournsize=len(pop))[0]
    starting_fitness = best_ind.fitness.values
   
    bestFit = []
    globalBest = float("inf")
    for g in range(iterations):
        if verbose:
            print("#################")
            print(f"generation {g}")
            print("#################")
        
        best_ind = tools.selTournament(pop, 1, tournsize=len(pop))[0]
        
        if verbose:
            print(best_ind)
            print(best_ind.fitness.values)
        if globalBest > best_ind.fitness.values[0]:
            globalBest = best_ind.fitness.values[0]
        bestFit += [(g, best_ind.fitness.values[0], globalBest)]
    
        offspring = toolbox.select(pop, len(pop))
        offspring = list(toolbox.map(toolbox.clone, offspring))
    
        for child1, child2 in zip(offspring[::2], offspring[1::2]):  #[x::2] takes every other element starting from x
            if random.random() < 0.3:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child1.fitness.values
    
        for mutant in offspring:
            if random.random() < 0.7:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        pop[:] = offspring

    return bestFit
    
    if verbose:
        print(f"starting fitness was {starting_fitness}")
        print(f"last best fitness {best_ind.fitness.values}")

if __name__ == "__main__":
    main()

