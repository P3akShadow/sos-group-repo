import random 
import numpy as np

knapsack_mean_default = 100.0
items_mean_default = 20.0
dimensions_default = 3

def generateInstance(numberOfKnapsacks, numberOfItems, knapsack_mean=knapsack_mean_default, items_mean=items_mean_default, dimensions=dimensions_default):
    knapsacks = np.random.exponential(knapsack_mean, (numberOfKnapsacks, dimensions))
    items = np.random.exponential(items_mean, (numberOfItems, dimensions))
    return(knapsacks, items)


def evaluate(knapsacks, items, order):
    capacities = knapsacks.copy()

    size = 0
    for pos in order:
        for i, capacityArr in enumerate(capacities):
            diff = capacities[i] - items[pos]
            if np.min(diff) >= 0:
                capacities[i] -= items[pos]
                size += np.prod(items[pos])
                break

    return (size, np.sum(capacities))

