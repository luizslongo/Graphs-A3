from grafoMatrizBipartido import GrafoMatrizAdjacenciaBipartido
from collections import deque

def hopcroft_karp(g: GrafoMatrizAdjacenciaBipartido):
    mate = {v: None for v in g.vertices}
    # print(mate)
    D = {}
    m = 0
    while bfs(g, mate, D):
        for x in g.X:
            if mate[x] is None:
                if dfs(g, mate, x, D):
                    m += 1
    return m, mate

def bfs(g, mate, D):
    Q = deque()
    for x in g.X:
        if mate[x] is None:
            D[x] = 0
            Q.append(x)
        else:
            D[x] = float('inf')
    D[None] = float('inf')

    while Q:
        x = Q.popleft()
        if D[x] < D[None]:
            for y in g.vizinhos(x):
                if D[mate[y]] == float('inf'):
                    D[mate[y]] = D[x] + 1
                    Q.append(mate[y])
    return D[None] != float('inf')

def dfs(g, mate, x, D):
    if x is not None:
        for y in g.vizinhos(x): 
            if D[mate[y]] == D[x] + 1:
                if dfs(g, mate, mate[y], D):
                    mate[y] = x
                    mate[x] = y
                    return True
        D[x] = float('inf')
        return False
    return True

if __name__ == '__main__':
    g = GrafoMatrizAdjacenciaBipartido()
    g.ler('A3/instancias/emparelhamento_maximo/pequeno.gr')
    # g.ler('A3/instancias/emparelhamento_maximo/pequeno2.gr')
    # # g.ler('A3/instancias/emparelhamento_maximo/gr128_10.gr')
    # # g.ler('A3/instancias/emparelhamento_maximo/gr256_30.gr')
    a = hopcroft_karp(g)
    print(a)

