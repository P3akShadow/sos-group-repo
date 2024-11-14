def c_optimize(antSys, max_iter=50, n_iter_no_change=10, verbose=True):
    '''
    Reimplementation of AntSystem.optimize() that returns a list containing the results for all iterations
    
    Details:
      An iterative optimization process that will stop if either the maximum total of iterations 
      (parameter max_iter) or the maximum number of iterations without updating the global best 
      (parameter n_iter_no_change) is reached.
      
    Parameters:
      * max_iter: the maximum total of iterations (default=50)
      * n_iter_no_change: the maximum number of iterations without update *g_best* (default=10)
      * verbose: show (True) or hide (False) optimization log (default=True)
    '''
    
    # Initialize the counter of iterations without *g_best* update
    count = 0
    
    result = []
    
    if verbose:
      # Show the log header
      print('| iter |         min        |         max        |        best        |')
    
    # For each optimization iteration
    s_iter = len(antSys.cost_history)+1
    f_iter = s_iter + max_iter
    for iter in range(s_iter, f_iter):
      ants = []
      # For each ant
      for ant in antSys.ants:
        # Create path
        cost = ant.create_path()

        # Update pheromone through the path
        ant.pheromone_update(antSys.phe_dep)
        
        # Store the ant and the cost of its current path
        ants.append((cost, ant))

      # Sort ants by the cost of its current path
      def sort_cost(e):
        return e[0]
      ants.sort(key=sort_cost)

      # Increase the pheromone through the elite's path
      n_elite_ants = round(antSys.elite_p_ants * len(ants))
      for i in range(n_elite_ants):
        ants[i][1].pheromone_update(antSys.phe_dep_elite)

      # Pheromone evaporation
      for edge in antSys.world.edges:
        edge.pheromone *= 1-antSys.evap_rate

      # Update global best (*g_best*)
      if antSys.g_best is None:
        antSys.g_best = (ants[0][0], ants[0][1].visited, ants[0][1].traveled)
      elif ants[0][0] < antSys.g_best[0]:
        count = 0
        antSys.g_best = (ants[0][0], ants[0][1].visited, ants[0][1].traveled)
      else:
        count+=1

      antSys.cost_history.append(antSys.g_best[0])  

      if verbose:
        # Show the log information of the current iteration
        print('|%6i|%20g|%20g|%20g|' % (iter, ants[0][0], ants[-1][0], antSys.g_best[0]))
      result.append((iter, ants[0][0], ants[-1][0], antSys.g_best[0]))
        
      # Finish the optimization process if *g_best* is not updated for n_iter_no_change iterations
      if count >= n_iter_no_change:
        break
    return result