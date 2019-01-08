#-*- coding: utf-8 -*-

from graph import *
from random import *
from gcp_local_search import *
from ecp_ls import *
import sys
import threading

file_path= "r125.1.col"

def createGraph(file):
    """
    parsing du fichier et creation du graphe
    """
    graph = Graph(0)
    for ligne in file:
        p =0
        if ligne.startswith("p"):
            line_data = ligne.split(" ")
            p = line_data[2]
            graph.set_n(int(p))
        if ligne.startswith("e"):
            edge= ligne.split(" ");
            graph.addEdge(int(edge[1]),int(edge[2]))
    file.close()
    return graph


def coloring_and_out(input_file_path,output_filepath,timemax):
    #file = open("dsjc250.5.col", "r")
    #print(file)

    with open(input_file_path, 'r') as fin:
        g=createGraph(fin)
        t = TabuEqcol(g, 7)
        coloring = t.search_minimum_coloring(0.7, 10, timemax)
        colors = ""
        for i in range(0, g.n):
             colors = colors + (str(get_colorof(i, coloring[1]))) + "  "
        f = open(output_filepath+".out", "w")
        f.write("K=" + str(coloring[0]) + "\n")
        f.write(colors)
        f.close()


if( len(sys.argv)>1):
    g = createGraph(open(sys.argv[1], "r"))
    #g.glouton_coloration()
    g.greedy_k_equitable(10)
else:
    coloring_and_out(file_path,file_path,5)
