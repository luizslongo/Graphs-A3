class GrafoListaAdjacencia:
    def __init__(self):
        self.vertices = set()
        self.arestas = {}
        self.pesos = {}
        self.nomes_vertices = {}

    def adicionarVertice(self, vertice: int) -> None:
        self.vertices.add(vertice)
        self.arestas[vertice] = []
        
    def adicionarAresta(self, u: int, v: int, peso: float = 1) -> None:
        self.arestas[u].append(v)
        self.pesos[(u, v)] = peso

    def qtdVertices(self) -> int:
        return len(self.vertices)

    def qtdArestas(self) -> int:
        return sum(len(vizinhos) for vizinhos in self.arestas.values()) // 2

    def grau(self, vertice: int) -> int:
        return len(self.arestas[vertice])

    def rotulo(self, vertice: int) -> str:
        return self.nomes_vertices.get(vertice, "Desconhecido")

    def vizinhos(self, vertice: int) -> list:
        return self.arestas[vertice]

    def haAresta(self, u: int, v: int) -> bool:
        return v in self.arestas[u]

    def peso(self, u: int, v: int) -> float:
        # https://wiki.python.org/moin/TimeComplexity
        # key in dict: O(1)
        if (u, v) in self.pesos:
            return self.pesos[(u, v)]
        else:
            return float('inf')
    
    def todosVerticesGrauPar(self) -> bool:
        for vertice in self.vertices:
            if self.grau(vertice) % 2 != 0:
                return False
        return True   
    
    def ler(self, arquivo: str) -> None:
        lendo_vertices = False
        nomes_vertices = {}  # Dicionário para armazenar os nomes dos vértices
        with open(arquivo, 'r') as f:
            for linha in f:
                partes = linha.strip().split()
                if partes:
                    if partes[0] == '*vertices':
                        lendo_vertices = True
                    elif partes[0] == '*edges' or partes[0] == '*arcs':
                        lendo_vertices = False
                    elif lendo_vertices:
                        vertice_num = int(partes[0])
                        if '"' in partes[1]:
                            nome_vertice = partes[1:]
                            nome_vertice = [string.replace('"', '') for string in nome_vertice]
                            nome_vertice_str = ''
                            for nome in nome_vertice:
                                nome_vertice_str += nome
                                nome_vertice_str += ' '
                            nome_vertice = nome_vertice_str[:-1]
                        else: 
                            nome_vertice = partes[1]
                        self.adicionarVertice(vertice_num)
                        nomes_vertices[vertice_num] = nome_vertice  # Armazena o nome no dicionário
                    else:
                        u, v, peso = (int(partes[0]), int(partes[1]), float(partes[2]))
                        self.adicionarAresta(u, v, peso)
                        # print(u, v, peso)

        self.nomes_vertices = nomes_vertices

    def exportar_mermaid(self) -> None:  
        # https://mermaid.live/
        # útil para visualizar grafos PEQUENOS (até 30 vértices)
        with open('export.mermaid', 'w+') as f:
            f.write("graph TD\n")
            for u in self.vertices:
                f.write(f"    {u}(({self.rotulo(u)}))\n")
            for u in self.vertices:
                for v in self.vizinhos(u):
                    if u < v:
                        f.write(f"    {u}<--{self.peso(u, v)}-->{v}\n")




if __name__ == '__main__':
    # Exemplo de uso
    grafo = GrafoListaAdjacencia()
    nome_arquivo = input("Digite o nome do arquivo .net: ")
    grafo.ler(nome_arquivo)
    print("Quantidade de vértices:", grafo.qtdVertices())
    print("Quantidade de arestas:", grafo.qtdArestas())
    print("Grau do vértice 1:", grafo.grau(1))
    print("Vizinhos do vértice 1:", grafo.vizinhos(1))
    print("Existe aresta entre 1 e 2?", grafo.haAresta(1, 2))
    print("Peso da aresta entre 1 e 2:", grafo.peso(1, 2))
    print("Rótulo do vértice 1:", grafo.rotulo(1))
    print("Rótulo do vértice 2:", grafo.rotulo(2))
    print(grafo.haAresta(1,2))
    grafo.exportar_mermaid()    
