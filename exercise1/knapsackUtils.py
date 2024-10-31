import random 
import numpy as np

knapsack_mean_default = 100.0

items_mean_default = 20.0

def generateInstance(numberOfKnapsacks, numberOfItems, knapsack_mean=knapsack_mean_default, items_mean=items_mean_default):
    knapsacks = np.random.exponential(knapsack_mean, numberOfKnapsacks)
    items = np.random.exponential(items_mean, numberOfItems)

    return(knapsacks, items)

