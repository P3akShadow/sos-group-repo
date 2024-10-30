#!/usr/bin/python3
import random

from rastriginUtils import rastrigin
from deap import base, creator, tools, algorithms

print(rastrigin([0,0,0]))
print(rastrigin([1,1,1]))


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

IND_SIZE = 5

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -4, 4)
toolbox.register("indiviual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)

ind1 = toolbox.indiviual()
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

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.8, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", lambda x:  [rastrigin(x)])


pop = [toolbox.indiviual() for _ in range(40)]
invalid_ind = [ind for ind in pop if not ind.fitness.valid]
fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
for ind, fit in zip(invalid_ind, fitnesses):
    ind.fitness.values = fit

for g in range(100):
    print("#################")
    print(f"generation {g}")
    print("#################")
    for ind in pop:
        print(ind.fitness)

    offspring = toolbox.select(pop, len(pop))
    offspring = list(toolbox.map(toolbox.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):  #[x::2] takes every other element starting from x
        if random.random() < 0.5:
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

