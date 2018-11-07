#-*- coding: utf-8 -*-


class Graph:
    """
    Represente un graphe non orienté, representé par une matrice d'adjascence
    ou une liste d'adjascence
    n:  le nombre de sommet du graphe
    m: le nombre d'arret du graphe
    """
    def __init__(self,n):
        self.g = []
        for i in range(0,n+1):
            self.g.append([])
        self.n = 0
        self.m = 0

    def addEdge(self,i,j):
        """
           Ajout d'un sommet au graphe
        """
        self.g[i].append(j)
        self.g[j].append(i)
        self.n+=1


    def print(self):
        for i in self.g:
            print(i)
            

