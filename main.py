#-*- coding: utf-8 -*-

from graph import *
from random import *
from gcp_local_search import *
from ecp_ls import *
import sys

file = open("dsjc250.5.col", "r") #chemin du fichier


def createGraph(file):
    """
    parsing du fichier et creation du graphe
    """
    for ligne in file:
        p =0;
        if ligne.startswith("p"):
            line_data = ligne.split(" ")
            p = line_data[2]
            graph = Graph(int(p))
        if ligne.startswith("e"):
            edge= ligne.split(" ");
            graph.addEdge(int(edge[1]),int(edge[2]))
    return graph
        


if( len(sys.argv)>1):
    g = createGraph(open(sys.argv[1], "r"))
    #g.glouton_coloration()
    g.greedy_k_equitable(10)
else:
    g = createGraph(file)
    #g.greedy_k_equitable(10)
    t = TabuCol(g,7)
    t2 = TabuEqcol(g,7)
    k = 50
    #print(t2.compute_solution(k,200,0.7,10))