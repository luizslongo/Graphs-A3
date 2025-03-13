class GrafoMatrizAdjacenciaBipartido:
    def __init__(self):
        self.vertices = set()
        self.matriz = [[float('inf')] for _ in range(1)]
        self.nomes_vertices = {}
        
        self.X = set()
        self.Y = set()

    def definir_lados_bipartido(self, X, Y):
        self.X = set(X)
        self.Y = set(Y)
        
    def adicionarVertice(self, vertice: int) -> None:
        self.vertices.add(vertice)
        for linha in self.matriz:
            linha.append(float('inf'))
        self.matriz.append([float('inf') for _ in range(len(self.matriz) + 1)])
    
    def adicionarAresta(self, u: int, v: int, peso: float) -> None:
        self.matriz[u][v] = peso
        self.matriz[v][u] = peso
    
    def qtdVertices(self) -> int:
        return len(self.vertices)
    
    def qtdArestas(self) -> int:
        # soma todos as arestas diferentes de infinito e divide por 2
        return sum(sum(1 for peso in linha if peso != float('inf')) for linha in self.matriz) // 2
    
    def grau(self, vertice: int) -> int:
        return sum(1 for peso in self.matriz[vertice] if peso != float('inf'))
    
    def rotulo(self, vertice: int) -> str:
        return self.nomes_vertices.get(vertice, "Desconhecido")
    
    def vizinhos(self, vertice: int) -> list:
        return [v for v in range(len(self.matriz[vertice])) if self.matriz[vertice][v] != float('inf')]
    
    def haAresta(self, u: int, v: int) -> bool:
        return self.matriz[u][v] != float('inf')
    
    def peso(self, u: int, v: int) -> float:
        return self.matriz[u][v]
    
    def getArestas(self):
        arestas = set()
        for i, linha in enumerate(self.matriz):
            for j, peso in enumerate(linha):
                if peso != float('inf'):
                    arestas.add((i, j))
        return arestas
    
    def ler(self, arquivo: str) -> None:
        with open(arquivo, 'r') as f:
            for linha in f:
                if linha.startswith('p'):
                    _, _, num_vertices, _ = linha.split()
                    num_vertices = int(num_vertices)
                    for i in range(1, num_vertices + 1):
                        self.adicionarVertice(i)
                elif linha.startswith('e'):
                    _, u, v = linha.split()
                    u, v = int(u), int(v)
                    self.adicionarAresta(u, v, 1)
                    if u not in self.X and u not in self.Y:
                        self.X.add(u)
                    if v not in self.X and v not in self.Y:
                        if u in self.X:
                            self.Y.add(v)
                        else:
                            self.X.add(v)

        # print(self.X, self.Y)

        
    def exportar_mermaid(self) -> None:
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
    grafo = GrafoMatrizAdjacencia()
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