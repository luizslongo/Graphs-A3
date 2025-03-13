class GrafoMatrizAdjacencia:
    def __init__(self):
        self.vertices = set()
        self.matriz = [[float('inf')] for _ in range(1)]
        self.nomes_vertices = {}
        
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
        lendo_vertices = False
        nomes_vertices = {}
        with open(arquivo, 'r') as f:
            for linha in f:
                partes = linha.strip().split()
                if partes:
                    if partes[0] == '*vertices':
                        lendo_vertices = True
                    elif partes[0] == '*edges':
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
                        nomes_vertices[vertice_num] = nome_vertice
                    else:
                        u, v, peso = (int(partes[0]), int(partes[1]), float(partes[2]))
                        self.adicionarAresta(u, v, peso)
                        # print(u, v, peso)
        
        self.nomes_vertices = nomes_vertices

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