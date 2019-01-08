#-*- coding: utf-8 -*-

import threading

class Graph:
    """
    Represente un graphe non orienté, representé par une liste d'adjascence
    ou une liste d'adjascence
    n:  le nombre de sommet du graphe
    m: le nombre d'arret du graphe
    """
    def __init__(self,n):
        self.g = []
        for i in range(0,n+1):
            self.g.append([])
        self.n = n
        self.m = 0
        self.coloration = (self.n+1)*[0]
        self.c = 1

    def addEdge(self,i,j):
        """
           Ajout d'un sommet au graphe
        """
        self.g[i].append(j)
        self.g[j].append(i)
        self.m+=1

    def set_n(self,val):
        self.__init__(val)


    def print(self):
        for i in self.g:
            print(i)


    def neighbors_colors(self, i):
        """
        :param i: l'indice de sommet
        :return: l'ensemble des coleurs des voisins du sommet
        """
        colors=[]
        for j in range(len(self.g[i])):
            colors.append(self.coloration[self.g[i][j]])
        return colors


    def glouton_coloration(self):
        """
        Coloration glouton:
        :return:
        """
        not_colored= []
        it=0

        for i in range(1,self.n+1):
            not_colored.append(i)
        while(not_colored!=[]):
            colored = []
            for k in range(len(not_colored)):
                node =not_colored[k]
                if not(self.c in self.neighbors_colors(node)):
                    self.coloration[node]=self.c
                    colored.append(node)
            for  k in colored:
                not_colored.remove(k)
            self.c=self.c+1
        self.c=self.c-1




    def size_color_class(self):
        size = (self.c+1)*[0]
        for i in range(1,self.c+1):
            size[i]=self.coloration.count(i)
        return size


    def isEquitableColoring(self,sizes):
        """
        Evuluation de l'equitabilité de la solution
        :param sizes: ensemble des nombre de sommets par classes de coloration
        :return: un booleen vrai renvoyé si la coloration est equitable
        """
        i=1
        equitable=True
        for i in range(1,len(sizes)):
            for j in range(1,len(sizes)):
                if abs(sizes[i]-sizes[j])>1:
                    return False
        return equitable

    def max_degree(self):
        """
        Le degré maximum du graphe
        :param i:
        :return: Vecteur de degrée de chaque sommet"
        """
        d=(self.n+1)*[0]
        for i in range(1,self.n+1):
            d[i]=len(self.g[i])
        return max(d)


    def get_vertices_of(self, col):
        """
        Recupère l'ensemble des sommets de la classe de couleur i
        :param i:
        :return:
        """
        Vi=[]

        for i in range(1,len(self.coloration)):
            if self.coloration[i]==col:
                Vi.append(i)
        return Vi



    def vertices_set_max(self):
        """
        L'ensemble de sommet de cardinal maximum
        :return:
        """

        class_color_size =self.size_color_class()
        max = class_color_size[1]
        i_max= 1
        for i in range(1,len(class_color_size)):
            if class_color_size[i]>max:
                i_max=i
                max = class_color_size[i]
        return i_max

    def vertices_set_min(self):
        """
        L'ensemble de couleur de cardinal minmum
        :return:
        """
        class_color_size = self.size_color_class()
        max = class_color_size[1]
        i_max = 1
        for i in range(1, len(class_color_size)):
            if class_color_size[i] < max:
                i_max = i
                max = class_color_size[i]
        return i_max



    def greedy_k_equitable(self, iter_max):
        self.glouton_coloration()
        class_color_size = self.size_color_class()
        cpt=0
        while not(self.isEquitableColoring(class_color_size)) :
            #la couleur de la frequence maximale
            col_max = self.vertices_set_max()
            col_min = self.vertices_set_min()
            V_max = self.get_vertices_of(col_max)
            V_min = self.get_vertices_of(col_min)
            ok = False
            i = 0
            while(ok==False and i<len(V_max)):
               if not(col_min in self.neighbors_colors(V_max[i])):
                   self.coloration[V_max[i]]=col_min
                   class_color_size = self.size_color_class()
                   ok =True
               i=i+1
            if ok==False:
                #nouvelle classe
                self.c=self.c+1
                self.coloration[V_max[0]] = self.c
                class_color_size = self.size_color_class()
            cpt=cpt+1
        print(len(class_color_size))




    def is_edge(self,i,j):
        """
        verifie s'il existe une arrete entre les sommet i et j du graphe
        :param j:
        :return:
        """
        return ( (j in(self.g[i])) or (i in(self.g[j])) )



















