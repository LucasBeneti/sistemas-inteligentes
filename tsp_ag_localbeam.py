import mlrose
import random
from timeit import default_timer as timer


dist_matrix = [[0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46], 
               [29, 0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21], 
               [82, 55, 0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51], 
               [46, 46, 68, 0, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
               [68, 42, 46, 82, 0, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
               [52, 43, 55, 15, 74, 0, 61, 23, 55, 31, 33, 37, 51, 29, 59],
               [72, 43, 23, 72, 23, 61, 0, 42, 23, 31, 77, 37, 51, 46, 33],
               [42, 23, 43, 31, 52, 23, 42, 0, 33, 15, 37, 33, 33, 31, 37],
               [51, 23, 41, 62, 21, 55, 23, 33, 0, 29, 62, 46, 29, 51, 11],
               [55, 31, 29, 42, 46, 31, 31, 15, 29, 0, 51, 55, 41, 23, 37],
               [29, 41, 79, 21, 82, 33, 77, 37, 62, 51, 0, 65, 42, 59, 61],
               [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65, 0, 61, 11, 55],
               [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61, 0, 62, 23],
               [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62, 0, 59],
               [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59, 0]]

# inicializando dist_list para o AG usar
dist_list = []
print(len(dist_matrix))
for i in range(len(dist_matrix)):
  for j in range(len(dist_matrix)):
    if(j>i):
      dist_list.append((i,j,dist_matrix[i][j]))

starting_row = random.randint(0,14)

"""
Beam Search
The width of the beam is the para o tamanho do feixe (valor k) e começa em um ponto aleatório
a partir de cada iteração se escolhe os k melhores vizinhos desse nó
inicial, e vai assim até o final. Até que todos os nós tenham sido visitado

from operator import itemgetter
k = 5
"""

to_visit_list = []
for i in range(len(dist_matrix)):
  to_visit_list.append(i)
print(to_visit_list)

def getStartingList(starting_node):
  """
  Main functionality is to return the list of nodes that need to be visited
  Parameters:
    startig_node: node to start from.
  """
  to_visit_list = []
  starting_list = []
  for i in range(len(dist_matrix)):
    to_visit_list.append(i)
  
  to_visit_list.remove(starting_row)
  for i, el in enumerate(dist_matrix[starting_row]):
    if(el != 0):
      starting_list.append((i,el))

  print(starting_list)
  starting_list.sort(key= lambda x: x[1])
  return starting_list

# passa a contagem de nodes visitados, node de início, lista de nodes para visitar
def findSmallestCostOnRow(node_row, to_visit_list, final_node_list=[], count=0):
  """
  The main use for this function is to find the best path from the given node. It works recursively until the stop condition is met.
  Parametes:
    node_row: node from where to start looking the best path
    to_visit_list: list of nodes to be visited
    final_node_list: node list that's passed and returned at the end of the recursive calling
    starting_node: passing on the starting node so it's possible to get some more clearer information at the end of the function
  """
  curr_node = node_row
  # print("Iteration: ", count)
  visits_count = count
  curr_to_visit_list = to_visit_list
  # print("Current visit list: ", curr_to_visit_list)
  curr_final_node_list = final_node_list

  if(visits_count == 13):
    print("returning this shit: ", curr_final_node_list)
    return curr_final_node_list
  else:
    curr_to_visit_list.remove(curr_node)
    aux_list = []
    for i, el in enumerate(curr_to_visit_list):
        aux_list.append((el,dist_matrix[curr_node][el]))
    # print(aux_list)
    # organiza a lista me ordem de custos
    aux_list.sort(key=lambda x: x[1])
    # chain resultante desse node
    curr_final_node_list.append(aux_list[0])
    visits_count += 1
    return findSmallestCostOnRow(count = visits_count, node_row = aux_list[0][0], to_visit_list = curr_to_visit_list, final_node_list = curr_final_node_list)


def resetVisitList(starting_node):
  """
  Parametes:
    starting_node: so it's possible to get the reset of the visited noteds list for the localBeamSearch function
  """
  to_visit_list = []
  for i in range(len(dist_matrix)):
    to_visit_list.append(i)

  to_visit_list.remove(starting_node)
  return to_visit_list

def getListOfSums(all_runs, starting_node):
  """
  Parametes:
    all_runs: list of all the chosen k-nodes, where each element is the best path from the node
    starting_node: passing on the starting node so it's possible to get some more clearer information at the end of the function
  """
  sum_by_run = []
  for run in all_runs:
    curr_sum = 0
    print(f"{starting_node} -> {run[0][0]}")
    for node in run:
      curr_sum += node[1]
    print(curr_sum)
    sum_by_run.append(curr_sum)

  print(f"Starting from {starting_node}th node, best run: going to node {all_runs[sum_by_run.index(min(sum_by_run))][0][0]} with run: {all_runs[sum_by_run.index(min(sum_by_run))]}")
  print(f"Total run cost: {min(sum_by_run)}")

  return sum_by_run

# k -> beam width
def localBeamSearch(k, starting_node):
  """
  Parametes:
    k: beam width
    starting_node: from wich node the search will start
  """
  starting_list = getStartingList(starting_node)
  ksmallest_nodes = starting_list[0:k]
  print(starting_list)
  print(ksmallest_nodes)
  all_runs = []
  really_final_list = []
  aux_list = []
  for node in ksmallest_nodes:
    to_visit = resetVisitList(starting_row)
    print(node[0])
    aux_list = findSmallestCostOnRow(node[0], to_visit,really_final_list)
    aux_list.insert(0,node)
    print(aux_list)
    really_final_list = []
    all_runs.append(aux_list)

  getListOfSums(all_runs, starting_row)


if __name__ == "__main__":
  k = input("Valor de k: ")
  mut_prob = input("Probabilidade de mutação: (em float)")
  max_att = input("Número de tentativas máximas: ")
  rnd_state=input("Random state inicial: (integer)")
  print("-------------------- Solving with Local Beam Search --------------------")
  start1 = timer()
  starting_node = random.randint(0,14)
  localBeamSearch(k, starting_node)
  end1 = timer()
  print("execution time: {0:.4f} s".format(end1-start1))

  print("")

  print("-------------------- Solving with Genetic Algorithm --------------------")
  start2= timer()
  # initilalizing fitness function object using dist_list
  fitness_dists = mlrose.TravellingSales(distances = dist_list)
  problem_no_fit = mlrose.TSPOpt(length=15, fitness_fn=fitness_dists, maximize=False)
  best_state, best_fitness = mlrose.genetic_alg(problem_no_fit,mutation_prob=mut_prob, max_attempts=max_att , random_state=rnd_state)
  print("Best state found is: ", best_state)
  print("Fitness at the best state: ", best_fitness)
  end2 = timer()
  print("execution time: {0:.4f} s".format(end2-start2))