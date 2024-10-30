#!/usr/bin/python3
import random

from rastriginUtils import rastrigin
from deap import base, creator, tools, algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

IND_SIZE = 5

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -4, 4)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)

ind1 = toolbox.individual()
print(ind1)
ind1.fitness.values = [rastrigin(ind1)]
print(ind1.fitness.valid)
print(ind1.fitness)

mutant = toolbox.clone(ind1)
ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.4, indpb=0.3)
del mutant.fitness.values

ind2.fitness.values = [rastrigin(ind2)]
print(ind2.fitness)

child1, child2 = [toolbox.clone(ind) for ind in (ind1, ind2)]

tools.cxBlend(child1, child2, 0.5)
del child1.fitness.values
del child2.fitness.values

selected = tools.selBest([child1, child2], 2)
offspring = [toolbox.clone(ind) for ind in selected]
