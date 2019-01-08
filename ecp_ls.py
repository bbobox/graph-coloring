from random import *
import copy
import threading


class TabuEqcol:

    def __init__(self,G,t):
        """
        :param G: le graphe
        :param t: le temps
        """
        self.g=G
        self.features = []
        self.tabu_list = []
        self.tenure = t
        self.live =[]

    def f(self, S):
        """
        Fonction objective
        :return:
        """
        cpt = 0
        for V in S:
            cpt += len(getEdges(V, self.g))
        return cpt



    def getbest_solution(self,S):
        fmax= self.f(S[0])
        sol= S[0]
        for s in S:
            if self.f(s)<fmax:
                sol=copyMatrix(s)
        return  sol

    def initial_solutionECp(self,k, G):
        """
        Generation de la solution initiale
        :param k: le nombre de sous ensemble V
        :return:
        """
        V = []
        for i in range(0, k):
            V.append([])
        vertices = []
        for i in range(0, G.n):
            vertices.append(i)

        n = G.n
        r = n - k * (n // k)
        rr = 0

        while (vertices != []):
            v = choice(vertices)
            I = []
            if rr < r:
                M = (n // k) + 1
            else:
                if rr >= r:
                    M = (n // k)

            for i in range(0, k):
                if len(V[i]) <= M - 1:
                    I.append(i)
            is_ok = False
            for i in range(0, len(I)):
                V[I[i]].append(v)
                if len(getEdges(V[I[i]], G)) == 0:
                    if len(V[I[i]]) == (n // k) + 1:
                        rr = rr + 1
                    is_ok = True
                    break
                else:
                    V[I[i]].remove(v)
            if is_ok == False:
                j = choice(I)
                V[j].append(v)
                if len(V[j]) == (n // k) + 1:
                    rr = rr + 1
            vertices.remove(v)
        return V

    def one_move(self,S, k,alpha,Beta):
        # choosing conflicting vertices
        C = get_conflicting_vectices(S, self.g)
        N = []
        cpt = 0
        sizeC=len(C)
        W_ = W_minus(S, self.g, k)
        for i in W_plus(S, self.g, k):
            for v in S[i]:
                if ((v in C) and not((v,i) in self.tabu_list)):
                    for j in W_:
                        N.append(copyMatrix(S))
                        N[cpt][i].remove(v)
                        N[cpt][j].append(v)
                        cpt = cpt + 1
                    if len(W_)>0:
                        self.tabu_list.append((v, i))
                        self.live[v][i] = alpha * sizeC + randrange(0, Beta)
        return N

    def exchange(self,S, k,alpha,Beta):
        """
        generation du Voisinage de la solution S
        :param S:
        :param G:
        :param k:
        :return:
        """
        C = get_conflicting_vectices(S,self.g)
        N = []
        cpt = 0
        sizeC = len(C)
        for vertex_v in C:
            col_v = get_colorof(vertex_v, S)
            if not((vertex_v,col_v) in self.tabu_list):
                for vertex_u in range(0, self.g.n):
                    col_u = get_colorof(vertex_u, S)
                    ok=False
                    if ((vertex_u!=vertex_v) and( (not(vertex_u in C) or (vertex_u>vertex_v)) )):
                        N.append(copyMatrix(S))
                        N[cpt][col_v].remove(vertex_v)
                        N[cpt][col_u].remove(vertex_u)
                        N[cpt][col_u].append(vertex_v)
                        N[cpt][col_v].append(vertex_u)
                        cpt = cpt + 1
                        ok=True
                    if(ok==True):
                        self.tabu_list.append((vertex_v, col_v))
                        self.live[vertex_v][col_v] = alpha * sizeC + randrange(0, Beta)

        return N


    def compute_solution(self,k,alpha, Beta):
        """
        Application de la la methode Taboue de recherche locale
        :param k:
        :param max:
        :param alpha:
        :param Beta:
        :return:
        """
        self.live = []
        self.tabu_list = []
        for i in range(self.g.n):
            self.live.append(k * [0])
        s0 =  copyMatrix(self.initial_solutionECp(k, self.g)) # Initial_solution
        currentS = copyMatrix(s0)
        bestS = copyMatrix(s0)
        global encore
        while (self.f(currentS)!= 0 and encore):
            for f in self.tabu_list:
                    v = f[0] # vertex v
                    c = f[1] # color c
                    self.live[v][c] =self.live[v][c]-1
                    if self.live[v][c]<=0:
                        self.tabu_list.remove(f)
            # Neighborhood
            N1= []
            if(self.g.n%k!=0):
                N1=self.one_move(currentS,k,alpha,Beta)
            N2=self.exchange(currentS,k,alpha,Beta)
            neighborhood = N1+N2
            if (neighborhood != []):
                currentS = self.getbest_solution(neighborhood)
                if self.f(currentS) < self.f(bestS):
                    bestS = copyMatrix(currentS)
        return (bestS, self.f(bestS))


    def search_minimum_coloring(self,alpha,Beta,time):
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
        timer = threading.Timer(time, findeboucle)
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
    for i in V:
        for j in V:
            if G.is_edge(i,j):
                E.append((i,j))

    return E




def W_plus(V,G,k):
    """
    L'ensemble de couleur de de card(c)=n/k+1
    :param k:
    :param G:
    :return:
    """
    C = get_conflicting_vectices(V, G)
    res = []
    for i in range(0, len(V)):
        if len(V[i]) == (G.n // k)+1:
            res.append(i)
    return res


def W_minus(V,G,k):
    """
    L'ensemble de couleur de de card(c)=n/k
    :param k:
    :param G:
    :return:
    """
    C = get_conflicting_vectices(V, G)
    res = []
    for i in range(0,len(V)):
        if (len(V[i]) == (G.n // k)):
            res.append(i)
    return res

def get_conflicting_vectices(S, G):
    C = []
    for i in range(0, len(S)):
        for j in getEdges(S[i], G):
            v1 = j[0]
            v2 = j[1]
            if not (v1 in C):
                C.append(v1)
            if not (v2 in C):
                C.append(v2)
    return C


def copyMatrix(M1):
    M=[]
    for i in range(len(M1)):
        M.append(M1[i][:])
    return M

def get_colorof(v, S):
    for i in range(len(S)):
        if v in S[i]:
            return i
    else:
        return -1