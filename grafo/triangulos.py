from grafo.base import Grafo


def contar_triangulos(g: Grafo) -> int:
    """Conta triângulos visitando cada trio de vértices uma única vez."""
    total = 0
    for u in g.vertices():
        for v in g.vizinhos(u):
            if v <= u:
                continue
            for w in g.vizinhos(v):
                if w <= v:
                    continue
                if g.tem_aresta(u, w):
                    total += 1
    return total
