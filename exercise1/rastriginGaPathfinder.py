#!/usr/bin/python3.10
#!/usr/bin/python3
import random

from rastriginUtils import rastrigin
from deap import base, creator, tools, algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def optimize(dimensions=5, population=40, iterations=1000):
    IND_SIZE = dimensions
    
    toolbox = base.Toolbox()
    
    toolbox.register("attr_float", random.uniform, -5.12, 5.12)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)
    
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.3, indpb=1.3/dimensions)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", lambda x:  [rastrigin(x)])

    pop = [toolbox.individual() for _ in range(population)]
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    bestFit = []
    
    globalBest = float("inf")
    for g in range(iterations):
        print("#################")
        print(f"generation {g}")
        print("#################")

        best_ind = tools.selTournament(pop, 1, tournsize=len(pop))[0]
        #for ind in pop:
            #print(ind.fitness)
        if best_ind.fitness.values[0] < globalBest:
            globalBest = best_ind.fitness.values[0]
        bestFit += [(g, best_ind.fitness.values[0], globalBest)]
    
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
    return bestFit

if __name__ == "__main__":
    print(optimize(dimensions=5, population=500, iterations=200))
