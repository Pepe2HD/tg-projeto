import networkx as nx

from grafo.lista import GrafoLista
from grafo.triangulos import contar_triangulos

# a, b, c, d, e, f viram os índices 0 a 5
ARESTAS = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)]

proprio = GrafoLista(6)
for u, v in ARESTAS:
    proprio.inserir_aresta(u, v)

referencia = nx.Graph()
referencia.add_nodes_from(range(6))
referencia.add_edges_from(ARESTAS)

assert proprio.ordem() == referencia.number_of_nodes()
assert proprio.tamanho() == referencia.number_of_edges()
assert contar_triangulos(proprio) == sum(nx.triangles(referencia).values()) // 3
