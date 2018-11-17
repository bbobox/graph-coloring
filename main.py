#-*- coding: utf-8 -*-

from graph import *
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
    g.greedy_k_equitable(10);
    #g.size_color_class()
    #print(g.max_degree())
else:
    g = createGraph(file)
    #g.glouton_coloration()
    
