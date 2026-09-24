from typing import Iterable

from grafo.base import Grafo


class GrafoLista(Grafo):
    def __init__(self, n: int) -> None:
        self._n = n
        self._m = 0
        self._adj: list[set[int]] = [set() for _ in range(n)]

    def ordem(self) -> int:
        return self._n

    def tamanho(self) -> int:
        return self._m

    def vizinhos(self, v: int) -> Iterable[int]:
        return iter(self._adj[v])

    def grau(self, v: int) -> int:
        return len(self._adj[v])

    def tem_aresta(self, u: int, v: int) -> bool:
        return v in self._adj[u]

    def inserir_aresta(self, u: int, v: int) -> None:
        if u == v:
            raise ValueError("laço não é permitido em grafo simples")
        if v in self._adj[u]:
            return
        self._adj[u].add(v)
        self._adj[v].add(u)
        self._m += 1
