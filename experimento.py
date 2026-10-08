import random
import time
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from grafo.matriz import GrafoMatriz
from grafo.lista import GrafoLista
from grafo.triangulos import contar_triangulos


# ==============================================================================
# ITEM 2: Teste de Corretude
# ==============================================================================
def testar_corretude():
    """Item 2: Valida as duas implementações com o grafo de exemplo (n=6, m=8)."""
    print("=== Executando Item 2: Teste de Corretude ===")
    arestas_exemplo = [
        (0, 1), (0, 2), (1, 2), (1, 3), 
        (2, 3), (2, 4), (3, 4), (4, 5)
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
        assert graus == [4, 3, 3, 3, 2, 1], f"Erro nos graus de {nome_classe}: {graus}"
        assert soma_graus == 2 * g.tamanho(), f"Erro no aperto de mão de {nome_classe}"
        assert triangulos == 3, f"Erro na contagem de triângulos de {nome_classe}"

        print(f"[OK] {nome_classe}: Ordem=6, Tamanho=8, Graus={graus}, Soma dos graus={soma_graus}")

    print("Todos os testes do Item 2 passaram com sucesso!\n")


# ==============================================================================
# ITENS 4 e 5: Geração Aleatória e Medição de Desempenho
# ==============================================================================
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
            mediana_tempo = tempos[1]  # O elemento central de 3 amostras é o índice 1

            print(f"{nome_classe:<15} | {rho:<15.3f} | {m:<12} | {espaco:<18} | {mediana_tempo:<18.5f}")

    print("\n")


# ==============================================================================
# ITEM 7: Leitura de Dataset Real com Tratamento de Erros e Métricas
# ==============================================================================
def ler_pares_com_erros(caminho: Path) -> Tuple[List[Tuple[str, str]], Dict[str, int]]:
    """
    Lê o arquivo de dataset e registra estatísticas de leitura,
    tratando exceções em linhas malformatadas ou corrompidas.
    """
    pares: List[Tuple[str, str]] = []
    relatorio = {
        "linhas_totais": 0,
        "linhas_ignoradas": 0,   # Linhas em branco ou comentários (#)
        "lacos_descartados": 0,  # Arestas do tipo u == v
        "erros_linhas": 0        # Linhas com formato inválido (< 2 colunas)
    }

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    for numero_linha, linha_raw in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
        relatorio["linhas_totais"] += 1
        linha = linha_raw.strip()

        # 1. Ignorar linhas vazias ou comentários
        if not linha or linha.startswith("#"):
            relatorio["linhas_ignoradas"] += 1
            continue

        # 2. Tratamento defensivo de erro ao processar colunas
        try:
            campos = linha.split()
            if len(campos) < 2:
                raise ValueError(f"Linha {numero_linha} possui menos de 2 elementos: '{linha}'")

            u, v = campos[0], campos[1]

            # 3. Descartar laços (u == v)
            if u == v:
                relatorio["lacos_descartados"] += 1
                continue

            pares.append((u, v))
        except Exception as err:
            relatorio["erros_linhas"] += 1

    return pares, relatorio


def indexar(pares: List[Tuple[str, str]]) -> Dict[str, int]:
    """Traduz cada rótulo distinto do arquivo em um índice contíguo 0..n-1."""
    indice: Dict[str, int] = {}
    for u, v in pares:
        for rotulo in (u, v):
            if rotulo not in indice:
                indice[rotulo] = len(indice)
    return indice


def construir(
    pares: List[Tuple[str, str]], 
    indice: Dict[str, int], 
    classe_grafo: Callable[[int], any]
) -> Tuple[any, int]:
    """Constrói o grafo e conta quantas arestas repetidas/duplicadas foram descartadas."""
    g = classe_grafo(len(indice))
    repetidas = 0
    antes = g.tamanho()

    for u, v in pares:
        g.inserir_aresta(indice[u], indice[v])
        if g.tamanho() == antes:
            repetidas += 1
        antes = g.tamanho()

    return g, repetidas


def conferir(g) -> Dict[str, any]:
    """Calcula estatísticas estruturais do grafo reconstruído."""
    n = g.ordem()
    m = g.tamanho()
    soma_graus = sum(g.grau(v) for v in g.vertices())
    isolados = sum(1 for v in g.vertices() if g.grau(v) == 0)
    maximo_arestas = (n * (n - 1)) / 2
    densidade = m / maximo_arestas if maximo_arestas > 0 else 0.0

    return {
        "n": n,
        "m": m,
        "soma_graus": soma_graus,
        "aperto_de_mao": soma_graus == 2 * m,
        "isolados": isolados,
        "densidade": densidade
    }


def criar_dataset_exemplo_se_nao_existir(caminho: Path):
    """Cria um arquivo de teste com caso de borda (comentários, laços, erros e duplicatas)."""
    if not caminho.exists():
        caminho.parent.mkdir(parents=True, exist_ok=True)
        conteudo = (
            "# Arquivo de teste para o Item 7\n"
            "# Formato: vertice_origem vertice_destino\n"
            "\n"
            "user1 user2\n"
            "user1 user3\n"
            "user2 user3\n"
            "user3 user3\n"  # Laço (deve ser descartado)
            "user1 user2\n"  # Aresta repetida (deve ser descartada)
            "linha_com_erro_solitaria\n"  # Linha inválida (deve gerar erro)
            "user3 user4\n"
            "user4 user5\n"
        )
        caminho.write_text(conteudo, encoding="utf-8")


def executar_item_7(caminho_arquivo: Path = Path("dados/dataset_real.edges")):
    """Executa o pipeline completo do Item 7 para um arquivo de dados real."""
    print("=== Executando Item 7: Leitura e Análise de Dataset Real ===")

    # Garante que um arquivo de exemplo exista caso não tenha baixado um ainda
    if not caminho_arquivo.exists():
        caminho_arquivo = Path("dados/exemplo.edges")
        criar_dataset_exemplo_se_nao_existir(caminho_arquivo)

    print(f"Lendo o arquivo: {caminho_arquivo}")

    # 1. Leitura com captura de relatório e erros
    pares, relatorio = ler_pares_com_erros(caminho_arquivo)

    # 2. Indexação de rótulos
    indice = indexar(pares)

    # 3. Construção do grafo (utilizando GrafoLista)
    g, arestas_repetidas = construir(pares, indice, GrafoLista)

    # 4. Conferência estrutural
    metricas = conferir(g)

    # 5. Exibição dos Resultados Formatados
    print("\n------------------------------------------------------------")
    print("RELATÓRIO DE LEITURA E TRATAMENTO DE DADOS (ITEM 7)")
    print("------------------------------------------------------------")
    print(f"Total de linhas lidas no arquivo : {relatorio['linhas_totais']}")
    print(f"Linhas ignoradas (# ou vazias) : {relatorio['linhas_ignoradas']}")
    print(f"Linhas com erros de formatação : {relatorio['erros_linhas']}")
    print(f"Laços descartados (u == v) : {relatorio['lacos_descartados']}")
    print(f"Arestas repetidas/duplicadas : {arestas_repetidas}")
    print("------------------------------------------------------------")
    print("MÉTRICAS DO GRAFO CONSTRUÍDO")
    print("------------------------------------------------------------")
    print(f"Número de rótulos distintos (n) : {len(indice)}")
    print(f"Ordem do Grafo (n) : {metricas['n']}")
    print(f"Tamanho do Grafo (m) : {metricas['m']}")
    print(f"Soma dos graus (sum d(v)) : {metricas['soma_graus']}")
    print(f"Validação Aperto de Mão (2m) : {'OK' if metricas['aperto_de_mao'] else 'FALHA'}")
    print(f"Vértices isolados (grau 0) : {metricas['isolados']}")
    print(f"Densidade calculada (rho) : {metricas['densidade']:.6f}")
    print("------------------------------------------------------------")

    # 6. Escolha e Justificativa da Representação
    rho = metricas['densidade']
    if rho < 0.1:
        sugestao = "GrafoLista (Lista de Adjacência)"
        justificativa = (
            f"O grafo é esparso (rho = {rho:.6f} < 0.1). A Lista de Adjacência economiza "
            f"memória alocando Theta(n + m) em vez de Theta(n^2), além de otimizar "
            f"a varredura de vizinhanças."
        )
    else:
        sugestao = "GrafoMatriz (Matriz de Adjacência)"
        justificativa = (
            f"O grafo é denso (rho = {rho:.6f} >= 0.1). A Matriz de Adjacência é preferível "
            f"pois permite testes de existência de arestas em tempo O(1) sem desperdício assintótico."
        )

    print("RECOMENDAÇÃO DE REPRESENTAÇÃO:")
    print(f"Estrutura indicada : {sugestao}")
    print(f"Justificativa : {justificativa}")
    print("============================================================\n")


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    testar_corretude()
    medir_experimento()
    executar_item_7()