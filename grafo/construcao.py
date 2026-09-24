from typing import Callable

from grafo.base import Grafo


def construir(
    pares: list[tuple[str, str]],
    indice: dict[str, int],
    criar: Callable[[int], Grafo],
) -> tuple[Grafo, int]:
    """Monta o grafo e devolve também quantas arestas repetidas foram vistas."""
    g = criar(len(indice))
    repetidas = 0
    antes = g.tamanho()
    for u, v in pares:
        g.inserir_aresta(indice[u], indice[v])
        if g.tamanho() == antes:
            repetidas += 1
        antes = g.tamanho()
    return g, repetidas
