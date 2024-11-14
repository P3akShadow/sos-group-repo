#!/usr/bin/python3

import numpy as np
from tspUtils import *
from deap import base, creator, tools
import random

cities = 50
instance = generateInstance(cities)
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
toolbox.register("select", tools.selTournament, tournsize=8)
toolbox.register("evaluate", lambda x: (evaluate(instance, x),))


pop = [toolbox.individual() for _ in range(40000)]
invalid_ind = [ind for ind in pop if not ind.fitness.valid]
fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
for ind, fit in zip(invalid_ind, fitnesses):
    ind.fitness.values = fit
best_ind = tools.selTournament(pop, 1, tournsize=len(pop))[0]
starting_fitness = best_ind.fitness.values

best_ind
for g in range(100):
    print("#################")
    print(f"generation {g}")
    print("#################")
    
    best_ind = tools.selTournament(pop, 1, tournsize=len(pop))[0]
    print(best_ind)
    print(best_ind.fitness.values)

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

print(f"starting fitness was {starting_fitness}")
print(f"last best fitness {best_ind.fitness.values}")
