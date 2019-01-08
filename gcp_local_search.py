from random import *
import copy
import threading



class TabuCol:

    def __init__(self, G, t):
        """

        :param G: le graphe
        :param t: le temps
        """
        self.g=G
        self.features = []
        self.tabu_list = []
        self.tenure = t
        self.live =[]



    def f(self,S):
        """
        Fonction objective
        :return:
        """
        cpt=0
        for V in S:
            cpt+=len(getEdges(V,self.g))
        return cpt

    def getbest_solution(self,S):
        fmax= self.f(S[0])
        sol= S[0]
        for s in S:
            if self.f(s)<fmax:
                sol=copyMatrix(s)
        return  sol

    def get_neighborhood(self, s,alpha, Beta):
        C = get_conflicting_vectices(s, self.g)
        vertices = []
        for i in range(0, len(s) + 1):
            vertices.append(i)
        sizeC= len(C)
        k = 0
        N = []
        for i in C:
            c = get_colorof(i, s)
            J = vertices[0:c] + vertices[c + 1:len(vertices) - 1]
            if not((i,c) in self.tabu_list):
                for j in J:
                    N.append(copyMatrix(s))
                    N[k][c].remove(i)
                    N[k][j].append(i)
                    k = k + 1
                self.tabu_list.append((i,c))
                self.live[i][c]= alpha *sizeC +randrange(0,Beta)
        return N


    def compute_solution(self,k,alpha, Beta):
        """

        :param k:
        :param max:
        :param alpha:
        :param Beta:
        :return:
        """
        self.live = []
        self.tabu_list=[]
        for i in range(self.g.n):
            self.live.append(k*[0])
        s0= initial_solution(k,self.g) #Initial_solution
        #print(s0)
        currentS=copyMatrix(s0)
        bestS= copyMatrix(s0)
        ok=False
        global encore
        while(self.f(currentS)!=0 and encore ):
          #  print("time =",time)
            for f in self.tabu_list:
                    v = f[0] # vertex v
                    c = f[1] # color c
                    #print(self.live[v][c])
                    if(v>self.g.n-1 or c>k-1):
                        print(v, c)
                    self.live[v][c] =self.live[v][c]-1
                    if self.live[v][c]<=0:
                        self.tabu_list.remove(f)

            #Neighborhood
            neighborhood = self.get_neighborhood(currentS,alpha,Beta)
            if(neighborhood!=[]):
                currentS= self.getbest_solution(neighborhood)
                if self.f(currentS)<self.f(bestS):
                    bestS=copyMatrix(currentS)
        return  (bestS,self.f(bestS))



    def search_minimum_coloring(self,alpha,Beta):
        """
        Rechrcherche coloration avec K minimal
        :return:
        """
        bestSol=[]
        bestK=0
        k= self.g.n
        iter = 0
        global encore
        encore = True
        timer = threading.Timer(200, findeboucle)
        timer.start()
        while(encore):
            tabus_search = self.compute_solution(k,alpha,Beta)
            if(tabus_search[1]==0):
                bestSol= copyMatrix(tabus_search[0])
                #tmax=tabus_search[2]
                bestK=k
                k=k-1
        return(bestK,bestSol)




def findeboucle():
    global encore
    encore = False



def getEdges(V,G):
    """

    :param V: Ensemble de sommets
    :return: la liste de d'arret
    """
    E=[]
    #print(V)
    for i in V:
        for j in V:
            if G.is_edge(i,j):
                E.append((i,j))

    return E


def initial_solution(k,G):
    """

    :param k: le nombre de sous ensemble V
    :return:
    """
    V=[]
    for i in range(0,k):
        V.append([])
    vertices=[]
    for i in range(0,G.n):
        vertices.append(i)

    while (vertices !=[]):
        v = choice(vertices)
        is_ok = False
        for i in range(0,k):
            V[i].append(v)
            if len(getEdges(V[i],G))==0:
                is_ok=True
                break
            else:
                V[i].remove(v)

        if is_ok==False:
            j = randrange(0,k)
            V[j].append(v)
        vertices.remove(v)

    return V




def get_features(n,V):
    features=[]
    for i in range(n+1):
        features.append(len(V)*[0])
    for i in range(0,len(V)):
        for j in V[i]:
            features[j][i]=1

    return features

def get_conflicting_vectices(S,G):
    C=[]
    for i in range(0,len(S)):
        for j in getEdges(S[i],G):
            v1=j[0]
            v2 = j[1]
            if not(v1 in C):
                C.append(v1)
            if not(v2 in C):
                C.append(v2)
    return C



def get_colorof(v,S):
    for i in range(len(S)):
        if v in S[i]:
            return i
    else:
        return -1




def copyMatrix(M1):
    M=[]
    for i in range(len(M1)):
        M.append(M1[i][:])
    return M


