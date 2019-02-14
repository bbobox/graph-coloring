#-*- coding: utf-8 -*-

from graph import *
from random import *
from ecp_ls import *
import sys
import threading

# import the necessary packages
import argparse


import sys, getopt, distutils
from distutils.util import strtobool

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


def coloring_and_out(file,timemax):
     with open(file,'r') as fin:
        g=createGraph(fin)
        t = TabuEqCol(g, 7)
        coloring = t.search_minimum_coloring(0.9, 5, timemax)
        print("k_min=",len(coloring.colorSet),coloring.colorSet)
        colors = ""
        for i in range(0, g.n):
             colors = colors + (str(get_colorof(i, coloring.colorSet))) + "  "
        f = open(file+".out", "w")
        f.write("K=" + str(len(coloring.colorSet)) + "\n")
        f.write(colors)
        f.close()


inputfile = ''
time=0
try:
  opts, args = getopt.getopt(sys.argv[1:], "i:t:h", ["inputfile=","time=" "help"])
except getopt.GetoptError:
    sys.exit(2)
    print('usage: main.py -i <inputfile> -t <time>')
for opt, arg in opts:
    if opt in ("-i", "--inputfile"):
      inputfile = arg
    elif opt in ("-t", "--time"):
        try:
            time = int(arg)
            print(time)
        except ValueError: print("-running time have integer value !")

if inputfile=='' or time==0:
    print('usage: main.py -i <inputfile> -t <time>')
    sys.exit(2)
g = createGraph(open(inputfile, "r"))
coloring_and_out( inputfile, time)
