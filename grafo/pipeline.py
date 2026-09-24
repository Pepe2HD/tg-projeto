from pathlib import Path

from grafo.construcao import construir
from grafo.conferencia import conferir
from grafo.leitura import indexar, ler_pares
from grafo.lista import GrafoLista

pares, relatorio = ler_pares(Path("dados/exemplo.edges"))
indice = indexar(pares)
g, repetidas = construir(pares, indice, GrafoLista)

print(relatorio)                       # linhas, ignoradas, lacos
print({"repetidas": repetidas})
print(conferir(g))                     # n, m, soma_graus, aperto_de_mao, ...
