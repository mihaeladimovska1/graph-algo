#Held-Karp Dynamic Programming Algorithm for Exact Solution of the sTSP Problem
#Written by: Mihaela Dimovska
#CS 594/690 Project 

#read the graph as input argument 
#the graph is symmetric (undirected) weighted graph in the DIMACS format
#if no weight between v_i and v_j, complete the graph by putting weight infinity = float(np.infty)
#if the graph is unweighted, generate random weights from uniform (1,100)


import sys
import string
import numpy as np
import itertools
import random
import math
import copy

file_object = open(sys.argv[1], 'r')
lines = file_object.readlines()
#delete the end-line character at the end of each read line
lines = [x.strip() for x in lines] 
val = lines[0].split('\t')
#print val
num_edges = int(val[1])
num_vertices = int(val[0])

#initialize the adj. matrix
adj_matrix = np.array([[0.0 for x in range(num_vertices)] for x in range(num_vertices)])

#form the adjacency matrix

for l in range(1, len(lines)):
    values = lines[l].split('\t')
    adj_matrix[int(values[0])-1][int(values[1])-1] = adj_matrix[int(values[1])-1][int(values[0])-1] = int(values[2]) 
    #if graph is unweighted, replace last equality with: 
    # np.random.randint(1,100)

#if graph is not complete
#add the infinity weigths
infty = float(np.inf)

for i in range(0, num_vertices):
    for j in range(i+1,num_vertices):
        if adj_matrix[i][j] == 0.0:
           adj_matrix[i][j] = adj_matrix[j][i] = infty

print adj_matrix
            
C_vals = {}
C_paths = {}
            
# local_opt: calculate the local optimum
def local_opt(start, subgraph, end, adj_matrix):
    if subgraph == set():
        C_vals[(frozenset(subgraph), end)] = adj_matrix[start][end]
        C_paths[(frozenset(subgraph), end)] = [start, end]
        return (adj_matrix[start][end], [start, end])
    else:
        temp_min_val = float(np.inf)
        temp_min_path = []
        partial_val = 0.0
        full_val = 0.0
        partial_path = []
        full_path = []
        for s in subgraph:
            if (frozenset(subgraph.difference(set([s]))), s) in C_vals:
                partial_val = C_vals[(frozenset(subgraph.difference(set([s]))), s)]
                partial_path = C_paths[(frozenset(subgraph.difference(set([s]))), s)]
                #print partial_path
            else:
                partial = local_opt(start, subgraph.difference(set([s])), s, adj_matrix)
                partial_val = partial[0]
                partial_path = partial[1]
                C_vals[(frozenset(subgraph.difference(set([s]))), s)] = partial_val
                C_paths[(frozenset(subgraph.difference(set([s]))), s)] = partial_path
                # print partial_path
                
            full_val = partial_val + adj_matrix[s][end]
            # print partial_path
            full_path = copy.deepcopy(partial_path)
            full_path.append(end)
            if full_val < temp_min_val:
                temp_min_val = full_val
                temp_min_path = full_path
        
        return (temp_min_val, temp_min_path)
        
# "outer" level: try every j not equal to root as a last vertex 
def TSP(num_vertices, adj_matrix, root):
    graph = set(range(num_vertices))
    
    temp_min_val = float(np.inf)
    temp_min_path = []
    
    for t in graph.difference(set([root])):
        partial = local_opt(root, graph.difference(set([root,t])), t, adj_matrix)
        full_val = partial[0] + adj_matrix[t][root]
        
        if full_val < temp_min_val:
            temp_min_val = full_val
            temp_min_path = copy.deepcopy(partial[1])
    
    return (temp_min_val, temp_min_path)

print TSP(num_vertices, adj_matrix, 0)
