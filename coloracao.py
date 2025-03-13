from grafoLista import GrafoListaAdjacencia
from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def conjuntos_independentes_maximais(G: GrafoListaAdjacencia):
    s = sorted(powerset(G.vertices), key=len, reverse=True) # 2^v, todos os subconjuntos possíveis na ordem descrescente
    # print(s)
    r = set()

    for x in s:
        c = True
        for v in x:
            for u in x:
                if u != v and G.haAresta(u, v):
                    c = False
                    break
        
        if c:
            subcj_x = powerset(x)
            # print(subcj_x)
            # remove subconjuntos de x de s
            for y in subcj_x:
                if y in s:
                    s.remove(y)
            r.add(x)

    return r

def subgrafo(G: GrafoListaAdjacencia, cj_vertices):
    g = GrafoListaAdjacencia()
    
    for vertice in cj_vertices:
        g.adicionarVertice(vertice)

    for u in cj_vertices:
        for v in cj_vertices:
            if u != v and G.haAresta(u, v):
                g.adicionarAresta(u, v)

    return g

def conjunto_para_indice(conjunto):
    # estou assumindo que os vértices são numerados de 1 a n nos exemplos
    soma = 0
    for i in conjunto:
        soma += 2**(i-1)

    return soma


def coloracao(G: GrafoListaAdjacencia):
    X = [None for _ in range(2**G.qtdVertices())]
    X[0] = 0

    SS = powerset(G.vertices)
    #print(f'2^v S: {SS}')

    for S in [x for x in SS if len(x) > 0]:
        s = conjunto_para_indice(S)

        X[s] = float('inf')

        g_linha = subgrafo(G, S)

        for I in conjuntos_independentes_maximais(g_linha):
            i = conjunto_para_indice([x for x in S if not x in I])

            #print(f'i: {i}, s: {s}, X[i]: {X[i]}, X[s]: {X[s]}')

            if X[i] + 1 < X[s]:
                X[s] = X[i] + 1

    return X[2**G.qtdVertices()-1]


if __name__ == '__main__':
    g = GrafoListaAdjacencia()
    g.ler('instancias/coloracao/cor3.net')

    a = coloracao(g)

    print(f'Coloração de instancias/coloracao/cor3.net: {a}')
