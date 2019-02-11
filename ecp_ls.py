from random import *
import copy
import threading


class ColoringSolution:
    """
    Representation d'une solution respectant la contrainte d'equité
    """
    def __init__(self,s,val,G):
        self.colorSet=copyMatrix(s)
        self.valueF= val
        self.features =[]
        self.g=G

    def set_valueF(self,f):
        self.valueF=f

    def copy(self):
        cpy= ColoringSolution(self.colorSet,self.valueF,self.g)
        cpy.features = self.features[:]
        return cpy




class TabuEqCol:

    def __init__(self,G,t):
        """
        :param G: le graphe
        :param t: le temps
        """
        self.g=G
        self.features = []
        self.tabu_list = []
        #self.tenure = t
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

    def neighborhood_filter(self,N, S):
        eval_s = S.valueF
        neighborhood_filtered=[]
        for solution_neighbor in N:
            if (not self.are_in_TabuList(solution_neighbor.features)==True):
                neighborhood_filtered.append(solution_neighbor)
        return neighborhood_filtered


    def are_in_TabuList(self,L):
        for feature in L:
            if self.live[feature[0]][feature[1]]>0:
                return True
        return False



    def getbest_solution(self,S):
        i_max=0
        fmax= S[i_max].valueF
        for i in range(0,len(S)):
            if S[i].valueF<fmax:
                i_max=i
                fmax= S[i_max].valueF

        return  S[i_max].copy()

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
                if rr == r:
                    M = (n // k)

            for i in range(0, k):
                if len(V[i]) <= M - 1:
                    I.append(i)
            is_ok = False
            for i in range(0, len(I)):
                conflicts_nb = len(getEdges(V[I[i]], G))
                V[I[i]].append(v)
                new_conflicts_nb = len(getEdges(V[I[i]], G))
                if new_conflicts_nb==conflicts_nb:
                    if len(V[I[i]]) == (n // k)+1:
                        rr = rr + 1
                    is_ok = True
                    break
                else:
                    V[I[i]].remove(v)
            if is_ok == False:
                j = choice(I)
                V[j].append(v)
                if len(V[j]) == (n // k)+1:
                    rr = rr + 1
            vertices.remove(v)

        init_sol= ColoringSolution(V,self.f(V),self.g)
        return init_sol

    def initSolPocess2(self,S,k, G):
        """
        Procedure 2 d'initilisation de la solution
        :param k:
        :param G:
        :return:
        """
        #newS=S.colorSet[0:k]
        #vertices=S.colorSet[k][:]
        #shuffle(newS)
        #-----------
        shuffle(S.colorSet)
        newS = S.colorSet[0:k]
        vertices = S.colorSet[k][:]
        rr=len(W_plus(newS,G,k))
        n = G.n
        r = n - k * (n // k)

        while(vertices!=[]):
            v=choice(vertices)
            I= []
            if rr < r:
                M = (n // k) + 1
            else:
                if rr == r:
                    M = (n // k)

            for i in range(0, k):
                if len(newS[i]) <= M - 1:
                    I.append(i)
            is_ok = False
            for i in range(0, len(I)):
                conflicts_nb = len(getEdges(newS[I[i]], G))
                newS[I[i]].append(v)
                new_conflicts_nb=len(getEdges(newS[I[i]], G))
                if new_conflicts_nb==conflicts_nb:
                    if len(newS[I[i]]) == (n // k) + 1:
                        rr = rr + 1
                    is_ok = True
                    break
                else:
                    newS[I[i]].remove(v)
            if is_ok == False:
                j = choice(I)
                newS[j].append(v)
                if len(newS[j]) == (n // k) + 1:
                    rr = rr + 1
            vertices.remove(v)

        init_sol = ColoringSolution(newS,self.f(newS),self.g)
        return init_sol




    def one_move(self,S, bestSol, k,alpha,Beta):
        # choosing conflicting vertices
        C = get_conflicting_vectices(S.colorSet, self.g)
        N = []
        cpt = 0
        sizeC=len(C)
        W_ = W_minus(S.colorSet, self.g, k)
        W_p= W_plus(S.colorSet, self.g, k)
        for i in W_p:
            for v in S.colorSet[i]:
                if (v in C) :
                    for j in W_:
                        Neighbor= copyMatrix(S.colorSet)
                        Neighbor[i].remove(v)
                        Neighbor[j].append(v)
                        neighbor = ColoringSolution(Neighbor,self.f(Neighbor),self.g)
                        neighbor.features.append((v,i))
                        if (self.are_in_TabuList([(v,j)]) == False) or neighbor.valueF<bestSol.valueF:
                            N.append(neighbor)

        return N

    def exchange(self,S, bestSol, k,alpha,Beta):
        """
        generation du Voisinage de la solution S
        :param S:
        :param G:
        :param k:
        :return:
        """
        C = get_conflicting_vectices(S.colorSet,self.g)
        N = []
        for vertex_v in C:
            col_v = get_colorof(vertex_v, S.colorSet)
            for vertex_u in range(0, self.g.n):
                col_u = get_colorof(vertex_u, S.colorSet)
                if ((vertex_u!=vertex_v) and( (not(vertex_u in C) or (col_u!=col_v)) ) ):
                    Neighbor =copyMatrix(S.colorSet)
                    v4 = len(getEdges(Neighbor[col_v], self.g))
                    v2 = len(getEdges(Neighbor[col_u], self.g))
                    Neighbor[col_v].remove(vertex_v)
                    Neighbor[col_u].remove(vertex_u)
                    Neighbor[col_u].append(vertex_v)
                    Neighbor[col_v].append(vertex_u)
                    v1=len(getEdges(Neighbor[col_v],self.g))
                    v3 = len(getEdges(Neighbor[col_u],self.g))
                    val = S.valueF-v2-v4+v3+v1
                    neighbor = ColoringSolution(Neighbor,val,self.g)
                    neighbor.features.append((vertex_v,col_v))
                    neighbor.features.append((vertex_u,col_u))
                    test = self.are_in_TabuList([(vertex_v,col_u),(vertex_u,col_v)])
                    if (test == False) or neighbor.valueF<bestSol.valueF:
                        N.append(neighbor)
        return N


    def compute_solution(self,k,alpha, Beta,previous_sol):
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
        if previous_sol.colorSet==[]:
            s0 = self.initial_solutionECp(k, self.g).copy()
        else:
            s0=  self.initSolPocess2(previous_sol,k,self.g).copy()
        currentS = s0.copy()
        bestS = s0.copy()
        global encore
        while (currentS.valueF!= 0 and encore):
            for f in self.tabu_list:
                    v = f[0] # vertex v
                    c = f[1] # color c
                    self.live[v][c] =self.live[v][c]-1
                    if self.live[v][c]<=0:
                        self.tabu_list.remove(f)
            # Neighborhood
            N1= []
            if(self.g.n%k!=0):
                N1=self.one_move(currentS,bestS,k,alpha,Beta)
            N2=self.exchange(currentS,bestS,k,alpha,Beta)
            neighborhood=[]
            neighborhood = N1+N2
            if (neighborhood != []):
                currentS =  self.getbest_solution(neighborhood).copy()
                sizeC = len(get_conflicting_vectices(currentS.colorSet, self.g))
                for feature in currentS.features:
                    if not(feature in self.tabu_list):
                        self.tabu_list.append(feature)
                    self.live[feature[0]][feature[1]] = alpha * sizeC + randrange(0, Beta)
                if currentS.valueF < bestS.valueF:
                    bestS = currentS.copy()
        return bestS


    def search_minimum_coloring(self,alpha,Beta,time):
        """
        Recherche de coloration avec K minimal
        :return:
        """
        bestSol=ColoringSolution([],0,self.g)
        currentBestSol=ColoringSolution([],0,self.g)
        bestK=0
        k= self.g.n
        global encore
        encore = True
        timer = threading.Timer(time, findeboucle)
        timer.start()
        while(encore):
            tabu_search = self.compute_solution(k,alpha,Beta,bestSol).copy()
            if(tabu_search.valueF==0):
                bestSol= tabu_search.copy()
                currentBestSol= tabu_search.copy()
                bestK=k
                k=k-1
        return currentBestSol

def findeboucle():
    global encore
    encore = False



def getEdges(V,G):
    """
    :param V: Ensemble de sommets
    :return: la liste de d'arret
    """
    E=[]
    n= len(V)
    for i in range(0,n):
        for j in range(i+1,n):
            if G.is_edge(V[i],V[j]):
                E.append((V[i],V[j]))

    return E




def W_plus(V,G,k):
    """
    L'ensemble de couleur de de card(c)=n/k+1
    :param k:
    :param G:
    :return:
    """
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

