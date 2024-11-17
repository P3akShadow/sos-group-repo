#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import time

import rastriginACO as rA
import knapsackACO as kA
import TSPACO as tA

import rastriginGaPathfinder as rG
import knapsackGaPathfinder as kG
import tspGaPathfinder as tG

# import random

# from tspUtils import generateInstance, evaluate

def main():
    #time_sos()
    plot()

def time_sos():
    verbose = False #do we want to print everything? 

    iterations = 5
    n = 2
    print("time for 5 ants iterations for rastrigin, n=2")
    t0= time.time()
    rA.train_ants(verbose=verbose, max_iterations=iterations, n=n)
    print(time.time() - t0)
    print("time for 5 GA generations for rastrigin, n=2")
    t0= time.time()
    rG.train_GA(verbose=verbose, iterations=iterations, dimensions=n)
    print(time.time() - t0)
    n = 3
    print("time for 5 ants iterations for rastrigin, n=3")
    t0= time.time()
    rA.train_ants(verbose=verbose, max_iterations=iterations, n=n)
    print(time.time() - t0)
    print("time for 5 GA generations for rastrigin, n=3")
    t0= time.time()
    rG.train_GA(verbose=verbose, iterations=iterations, dimensions=n)
    print(time.time() - t0)
    n = 5
    print("time for 5 ants iterations for rastrigin, n=5")
    t0= time.time()
    rA.train_ants(verbose=verbose, max_iterations=iterations, n=n)
    print(time.time() - t0)
    print("time for 5 GA generations for rastrigin, n=5")
    t0= time.time()
    rG.train_GA(verbose=verbose, iterations=iterations, dimensions=n)
    print(time.time() - t0)

    num_knapsacks = 1
    num_items = 10
    dim=1
    print("time for 5 ants iterations for knapsack, ks=1, i=10,n=1")
    t0= time.time()
    kA.train_ants(verbose=verbose, num_knapsacks=num_knapsacks, num_items=num_items, max_iterations=iterations, dim=dim)
    print(time.time() - t0)
    print("time for 5 GA generations for knapsack, ks=1, i=10,n=1")
    t0= time.time()
    kG.train_GA(verbose=verbose, knapsacks=num_knapsacks, items=num_items, iterations=iterations, dim=dim)
    print(time.time() - t0)
    num_knapsacks = 5
    num_items = 50
    dim=2
    print("time for 5 ants iterations for knapsack, ks=5, i=50,n=2")
    t0= time.time()
    kA.train_ants(verbose=verbose, num_knapsacks=num_knapsacks, num_items=num_items, max_iterations=iterations, dim=dim)
    print(time.time() - t0)
    print("time for 5 GA generations for knapsack, ks=5, i=50,n=2")
    t0= time.time()
    kG.train_GA(verbose=verbose, knapsacks=num_knapsacks, items=num_items, iterations=iterations, dim=dim)
    print(time.time() - t0)
    num_knapsacks = 10
    num_items = 100
    dim=3
    print("time for 5 ants iterations for knapsack, ks=10, i=100,n=3")
    t0= time.time()
    kA.train_ants(verbose=verbose, num_knapsacks=num_knapsacks, num_items=num_items, max_iterations=iterations, dim=dim)
    print(time.time() - t0)
    print("time for 5 GA generations for knapsack, ks=10, i=100,n=3")
    t0= time.time()
    kG.train_GA(verbose=verbose, knapsacks=num_knapsacks, items=num_items, iterations=iterations, dim=dim)
    print(time.time() - t0)

    cities = 10
    print("time for 5 ants iterations for tsp, cities=10")
    t0= time.time()
    tA.train_ants(verbose=verbose,num_cities=cities, max_iterations=iterations)
    print(time.time() - t0)
    print("time for 5 GA generations for tsp, cities=10")
    t0= time.time()
    tG.train_GA(verbose=verbose, cities=cities, iterations=iterations)
    print(time.time() - t0)
    cities = 20
    print("time for 5 ants iterations for tsp, cities=20")
    t0= time.time()
    tA.train_ants(verbose=verbose,num_cities=cities, max_iterations=iterations)
    print(time.time() - t0)
    print("time for 5 GA generations for tsp, cities=20")
    t0= time.time()
    tG.train_GA(verbose=verbose, cities=cities, iterations=iterations)
    print(time.time() - t0)
    cities = 50
    print("time for 5 ants iterations for tsp, cities=50")
    t0= time.time()
    tA.train_ants(verbose=verbose,num_cities=cities, max_iterations=iterations)
    print(time.time() - t0)
    print("time for 5 GA generations for tsp, cities=50")
    t0= time.time()
    tG.train_GA(verbose=verbose, cities=cities, iterations=iterations)
    print(time.time() - t0)

    print("---------------timing done!--------------")
    print("-----------------------------------------")
    

def plot():
    verbose = True #do we want to print everything? 
    iterations = 30
    
    plot1 = plt.subplot2grid((3, 1), (0, 0))
    plot2 = plt.subplot2grid((3, 1), (1, 0))
    plot3 = plt.subplot2grid((3, 1), (2, 0))

    n = 5
    t0= time.time()
    rastrigin_ants = np.array(rA.train_ants(verbose=verbose, max_iterations=iterations, n=n))
    print(time.time() - t0)
    t0= time.time()
    rastrigin_GA = np.array(rG.train_GA(verbose=verbose, iterations=iterations, dimensions=n))
    print(time.time() - t0)
    x_a = rastrigin_ants[:, 0].astype(int)
    x_g = rastrigin_GA[:, 0].astype(int)
    plot1.plot(x_a, rastrigin_ants[:, 1], color="green", label="current best ants") #current best
    plot1.plot(x_a, rastrigin_ants[:, 2], color="blue", label="global best ants")  #global best
    plot1.plot(x_g, rastrigin_GA[:, 1], color="red", label="current best GA") #current best
    plot1.plot(x_g, rastrigin_GA[:, 2], color="orange", label="global best GA")  #global best
    plot1.set_title("Rastrigin for n=%d" % n)
    plot1.set_xlabel("Iteration/Generation")
    plot1.set_ylabel("rastrigin value")

    print("calc knapsacks")
    num_knapsacks = 10
    num_items = 100
    dim=3
    knapsack_ants = np.array(kA.train_ants(verbose=verbose, num_knapsacks=num_knapsacks, num_items=num_items, max_iterations=iterations,dim=dim))
    knapsack_GA = np.array(kG.train_GA(verbose=verbose, knapsacks=num_knapsacks, items=num_items, iterations=iterations,dim=dim))
    x_a = knapsack_ants[:, 0].astype(int)
    x_g = knapsack_GA[:, 0].astype(int)
    plot2.plot(x_a, 1/knapsack_ants[:, 1], color="green", label="current best ants") #current best
    plot2.plot(x_a, 1/knapsack_ants[:, 2], color="blue", label="global best ants")  #global best
    plot2.plot(x_g, knapsack_GA[:, 1], color="red", label="current best GA") #current best
    plot2.plot(x_g, knapsack_GA[:, 2], color="orange", label="global best GA")  #global best
    plot2.set_title("Knapsack for %d knapsacks and %d items of dim=%d" % (num_knapsacks, num_items, dim))
    plot2.set_xlabel("Iteration/Generation")
    plot2.set_ylabel("total knapsack value")

    cities = 50
    tsp_ants = np.array(tA.train_ants(verbose=verbose,num_cities=cities, max_iterations=iterations))
    tsp_GA = np.array(tG.train_GA(verbose=verbose, cities=cities, iterations=iterations))
    x_a = tsp_ants[:, 0].astype(int)
    x_g = tsp_GA[:, 0].astype(int)
    plot3.plot(x_a, tsp_ants[:, 1], color="green", label="current best ants") #current best
    plot3.plot(x_a, tsp_ants[:, 2], color="blue", label="global best ants")  #global best
    plot3.plot(x_g, tsp_GA[:, 1], color="red", label="current best GA") #current best
    plot3.plot(x_g, tsp_GA[:, 2], color="orange", label="global best GA")  #global best
    plot3.set_title("TSP for %d citites" % cities)
    plot3.set_xlabel("Iteration/Generation")
    plot3.set_ylabel("shortest path length")

    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.show()

if __name__ == '__main__':
    main()
