from grafo.base import Grafo


def conferir(g: Grafo) -> dict[str, int | float | bool]:
    """Devolve medidas que permitem conferir um grafo recém-lido."""
    n = g.ordem()
    m = g.tamanho()
    soma_graus = sum(g.grau(v) for v in g.vertices())
    isolados = sum(1 for v in g.vertices() if g.grau(v) == 0)
    maximo = n * (n - 1) / 2
    return {
        "n": n,
        "m": m,
        "soma_graus": soma_graus,
        "aperto_de_mao": soma_graus == 2 * m,
        "isolados": isolados,
        "densidade": m / maximo if maximo > 0 else 0.0,
    }
