import random
import time
from grafo.matriz import GrafoMatriz
from grafo.lista import GrafoLista
from grafo.triangulos import contar_triangulos


def testar_corretude():
    """Item 2: Valida as duas implementações com o grafo de exemplo (n=6, m=8)."""
    print("=== Executando Item 2: Teste de Corretude ===")

    arestas_exemplo = [
        (0, 1), (0, 2), (1, 2),
        (1, 3), (2, 3), (2, 4),
        (3, 4), (4, 5)
    ]

    for nome_classe, classe in [("GrafoMatriz", GrafoMatriz), ("GrafoLista", GrafoLista)]:
        g = classe(6)

        for u, v in arestas_exemplo:
            g.inserir_aresta(u, v)

        graus = sorted([g.grau(v) for v in g.vertices()], reverse=True)
        soma_graus = sum(g.grau(v) for v in g.vertices())
        triangulos = contar_triangulos(g)

        assert g.ordem() == 6, f"Erro na ordem de {nome_classe}"
        assert g.tamanho() == 8, f"Erro no tamanho de {nome_classe}"
        
        # Graus esperados: [4, 3, 3, 3, 2, 1]
        assert graus == [4, 3, 3, 3, 2, 1], f"Erro nos graus de {nome_classe}: {graus}"
        
        assert soma_graus == 2 * g.tamanho(), f"Erro no aperto de mão de {nome_classe}"
        assert triangulos == 3, f"Erro na contagem de triângulos de {nome_classe}"

        print(f"[OK] {nome_classe}: Ordem=6, Tamanho=8, Graus={graus}, Triângulos={triangulos}")

    print("Todos os testes do Item 2 passaram com sucesso!\n")


def gerar_grafo_aleatorio(classe, n: int, rho: float, seed: int = 42):
    """Item 4: Gera grafo aleatório de ordem n e densidade rho."""
    random.seed(seed)
    g = classe(n)

    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < rho:
                g.inserir_aresta(u, v)

    return g


def medir_experimento():
    """Itens 4 e 5: Medição de tempo e espaço nas 3 densidades."""
    print("=== Executando Itens 4 e 5: Medições de Desempenho (n = 2000) ===")

    n = 2000
    densidades = [0.001, 0.05, 0.5]

    print(f"{'Estrutura':<15} | {'Densidade (rho)':<15} | {'Arestas (m)':<12} | {'Espaço (posições)':<18} | {'Tempo Mediano (s)':<18}")
    print("-" * 90)

    for rho in densidades:
        for nome_classe, classe in [("GrafoMatriz", GrafoMatriz), ("GrafoLista", GrafoLista)]:
            g = gerar_grafo_aleatorio(classe, n, rho)
            m = g.tamanho()

            # Cálculo de espaço
            if nome_classe == "GrafoMatriz":
                espaco = n * n
            else:
                espaco = n + 2 * m

            # Medição de tempo (mediana de 3 execuções)
            tempos = []
            for _ in range(3):
                t0 = time.perf_counter()
                _ = contar_triangulos(g)
                t1 = time.perf_counter()
                tempos.append(t1 - t0)

            tempos.sort()
            mediana_tempo = tempos[1]  # índice correto da mediana

            print(f"{nome_classe:<15} | {rho:<15.3f} | {m:<12} | {espaco:<18} | {mediana_tempo:<18.5f}")


if __name__ == "__main__":
    testar_corretude()
    medir_experimento()