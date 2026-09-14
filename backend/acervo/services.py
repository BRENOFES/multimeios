from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from alunos.models import Aluno
from gestao.models import Administrador
from .domain import (
    estoque_apos_devolucao,
    estoque_apos_emprestimo,
    validar_devolucao,
)
from .models import Emprestimo, Livro


class RegraEmprestimo(ValueError):
    pass


def criar_emprestimo(*, usuario_id, admin_id, livro_id, prazo_dias=7):
    try:
        prazo_dias = int(prazo_dias)
    except (TypeError, ValueError) as exc:
        raise RegraEmprestimo("O prazo precisa ser um número inteiro.") from exc
    if not 1 <= prazo_dias <= 60:
        raise RegraEmprestimo("O prazo precisa ficar entre 1 e 60 dias.")

    aluno = Aluno.objects.using("usuarios").filter(pk=usuario_id).first()
    if aluno is None:
        raise RegraEmprestimo("Aluno não encontrado.")

    administrador = (
        Administrador.objects.using("admin_db").filter(pk=admin_id).first()
    )
    if administrador is None:
        raise RegraEmprestimo("Administrador não encontrado.")

    hoje = timezone.localdate()
    with transaction.atomic(using="default"):
        livro = (
            Livro.objects.using("default")
            .select_for_update()
            .filter(pk=livro_id)
            .first()
        )
        if livro is None:
            raise RegraEmprestimo("Livro não encontrado.")

        try:
            livro.quantidade_disponivel = estoque_apos_emprestimo(
                livro.quantidade_total,
                livro.quantidade_disponivel,
            )
        except ValueError as exc:
            raise RegraEmprestimo(str(exc)) from exc

        emprestimo = Emprestimo.objects.using("default").create(
            usuario_id=aluno.id,
            admin_id=administrador.id,
            livro=livro,
            aluno_nome=aluno.nome,
            data_aluguel=hoje,
            data_prevista=hoje + timedelta(days=prazo_dias),
            status=Emprestimo.Status.ALUGADO,
        )
        livro.save(using="default", update_fields=["quantidade_disponivel"])

    return emprestimo


def devolver_emprestimo(*, emprestimo_id):
    hoje = timezone.localdate()
    with transaction.atomic(using="default"):
        emprestimo = (
            Emprestimo.objects.using("default")
            .select_for_update()
            .select_related("livro")
            .filter(pk=emprestimo_id)
            .first()
        )
        if emprestimo is None:
            raise RegraEmprestimo("Empréstimo não encontrado.")

        try:
            validar_devolucao(emprestimo.status)
        except ValueError as exc:
            raise RegraEmprestimo(str(exc)) from exc

        livro = (
            Livro.objects.using("default")
            .select_for_update()
            .get(pk=emprestimo.livro_id)
        )
        try:
            livro.quantidade_disponivel = estoque_apos_devolucao(
                livro.quantidade_total,
                livro.quantidade_disponivel,
            )
        except ValueError as exc:
            raise RegraEmprestimo(str(exc)) from exc

        emprestimo.status = Emprestimo.Status.DEVOLVIDO
        emprestimo.data_recebimento = hoje
        emprestimo.save(
            using="default",
            update_fields=["status", "data_recebimento"],
        )
        livro.save(using="default", update_fields=["quantidade_disponivel"])

    return emprestimo


def atualizar_emprestimos_atrasados():
    return (
        Emprestimo.objects.using("default")
        .filter(
            status=Emprestimo.Status.ALUGADO,
            data_prevista__lt=timezone.localdate(),
        )
        .update(status=Emprestimo.Status.ATRASADO)
    )
