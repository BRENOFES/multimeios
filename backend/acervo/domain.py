STATUS_EM_ABERTO = {"alugado", "atrasado"}


def estoque_apos_emprestimo(quantidade_total, quantidade_disponivel):
    if quantidade_total < 1:
        raise ValueError("A quantidade total precisa ser positiva.")
    if quantidade_disponivel < 1:
        raise ValueError("Não há exemplar disponível.")
    if quantidade_disponivel > quantidade_total:
        raise ValueError("O estoque disponível está inconsistente.")
    return quantidade_disponivel - 1


def estoque_apos_devolucao(quantidade_total, quantidade_disponivel):
    if quantidade_total < 1 or quantidade_disponivel < 0:
        raise ValueError("O estoque está inconsistente.")
    if quantidade_disponivel >= quantidade_total:
        raise ValueError("Todos os exemplares já estão disponíveis.")
    return quantidade_disponivel + 1


def validar_devolucao(status):
    if status not in STATUS_EM_ABERTO:
        raise ValueError("Este empréstimo já foi devolvido.")
