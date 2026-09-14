def calcular_proxima_serie(serie):
    """Retorna a próxima série; None representa conclusão do 3º ano."""
    if serie not in (1, 2, 3):
        raise ValueError("A série precisa estar entre 1 e 3.")
    return None if serie == 3 else serie + 1
