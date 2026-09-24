from pathlib import Path


def ler_pares(caminho: Path) -> tuple[list[tuple[str, str]], dict[str, int]]:
    """Lê o arquivo e devolve os pares de rótulos e um relatório da leitura."""
    pares: list[tuple[str, str]] = []
    relatorio = {"linhas": 0, "ignoradas": 0, "lacos": 0}
    for numero, linha in enumerate(caminho.read_text().splitlines(), start=1):
        relatorio["linhas"] += 1
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            relatorio["ignoradas"] += 1
            continue
        campos = linha.split()
        if len(campos) < 2:
            raise ValueError(f"linha {numero} não tem dois vértices: {linha!r}")
        u, v = campos[0], campos[1]
        if u == v:
            relatorio["lacos"] += 1
            continue
        pares.append((u, v))
    return pares, relatorio


def indexar(pares: list[tuple[str, str]]) -> dict[str, int]:
    """Traduz cada rótulo distinto em um índice de 0 a n-1, na ordem de
    primeira aparição."""
    indice: dict[str, int] = {}
    for u, v in pares:
        for rotulo in (u, v):
            if rotulo not in indice:
                indice[rotulo] = len(indice)
    return indice
