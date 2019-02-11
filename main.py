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
            edge= ligne.split(" ")
            graph.addEdge(int(edge[1])-1,int(edge[2])-1)
    file.close()
    return graph


def coloring_and_out(input_file_path,output_filepath,timemax):
     with open(input_file_path, 'r') as fin:
        g=createGraph(fin)
        t = TabuEqCol(g, 7)
        coloring = t.search_minimum_coloring(0.9, 5, timemax)
        print("k_min=",len(coloring.colorSet),coloring.colorSet)
        colors = ""
        for i in range(0, g.n):
             colors = colors + (str(get_colorof(i, coloring.colorSet))) + "  "
        f = open("output_files_3600/"+output_filepath+".out", "w")
        f.write("K=" + str(len(coloring.colorSet)) + "\n")
        f.write(colors)
        f.close()


if( len(sys.argv)>1):
    n= len(sys.argv)
    files=[]
    for i in range(1,n):
        g = createGraph(open(sys.argv[i], "r"))
        coloring_and_out(sys.argv[i], sys.argv[i], 3600)
else:
    print("aucun fichier en paramètre")
    #coloring_and_out(file_path,file_path,5)
