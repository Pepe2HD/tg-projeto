from typing import Iterable

from grafo.base import Grafo


class GrafoMatriz(Grafo):
    def __init__(self, n: int) -> None:
        self._n = n
        self._m = 0
        self._a = [[0] * n for _ in range(n)]

    def ordem(self) -> int:
        return self._n

    def tamanho(self) -> int:
        return self._m

    def vizinhos(self, v: int) -> Iterable[int]:
        return (u for u in range(self._n) if self._a[v][u] == 1)

    def tem_aresta(self, u: int, v: int) -> bool:
        return self._a[u][v] == 1

    def inserir_aresta(self, u: int, v: int) -> None:
        if u == v:
            raise ValueError("laço não é permitido em grafo simples")
        if self._a[u][v] == 1:
            return
        self._a[u][v] = 1
        self._a[v][u] = 1
        self._m += 1
