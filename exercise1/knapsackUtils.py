import random 
import numpy as np

knapsack_mean_default = 100.0
items_mean_default = 20.0
dimensions_default = 3

def generateInstance(numberOfKnapsacks, numberOfItems, knapsack_mean=knapsack_mean_default, items_mean=items_mean_default, dimensions=dimensions_default, seed=1):
    np.random.seed(seed)
    knapsacks = np.random.exponential(knapsack_mean, (numberOfKnapsacks, dimensions))
    items = np.random.exponential(items_mean, (numberOfItems, dimensions+1))
    return(knapsacks, items)


def evaluate(knapsacks, items, order, verbose=False):
    capacities = knapsacks.copy()

    size = 0
    for pos in order:
        for i, capacityArr in enumerate(capacities):
            diff = capacities[i] - items[pos][1:]
            if np.min(diff) >= 0:
                if verbose:
                    print(f"knapsack {i} takes in value {items[pos][0]} of cost {items[pos][1:]}")
                capacities[i] -= items[pos][1:]
                size += np.sum(items[pos][0])
                #size += np.product(items[pos])
                break

    return (size, np.sum(capacities))

