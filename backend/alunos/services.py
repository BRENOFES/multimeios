from django.db import DatabaseError

from acervo.models import Emprestimo
from .domain import calcular_proxima_serie
from .models import Aluno


STATUS_ATIVOS = (
    Emprestimo.Status.ALUGADO,
    Emprestimo.Status.ATRASADO,
)


def progredir_alunos(turmas_por_aluno=None):
    """Promove os alunos e remove concluintes sem empréstimos ativos."""
    turmas_por_aluno = {
        str(chave): valor for chave, valor in (turmas_por_aluno or {}).items()
    }
    resultado = {"promovidos": [], "formados": [], "bloqueados": []}

    for aluno in Aluno.objects.using("usuarios").all().order_by("id"):
        proxima_serie = calcular_proxima_serie(aluno.serie)

        if proxima_serie is None:
            possui_pendencia = Emprestimo.objects.using("default").filter(
                usuario_id=aluno.id,
                status__in=STATUS_ATIVOS,
            ).exists()
            if possui_pendencia:
                resultado["bloqueados"].append(
                    {
                        "id": aluno.id,
                        "nome": aluno.nome,
                        "motivo": "empréstimo ativo",
                    }
                )
                continue

            try:
                aluno.delete(using="usuarios")
            except DatabaseError:
                resultado["bloqueados"].append(
                    {
                        "id": aluno.id,
                        "nome": aluno.nome,
                        "motivo": "restrição no banco; revise as FKs instaladas",
                    }
                )
            else:
                resultado["formados"].append({"id": aluno.id, "nome": aluno.nome})
            continue

        aluno.serie = proxima_serie
        nova_turma = turmas_por_aluno.get(str(aluno.id))
        if nova_turma:
            aluno.turma = str(nova_turma).strip()
        aluno.full_clean()
        aluno.save(using="usuarios", update_fields=["serie", "turma"])
        resultado["promovidos"].append(
            {
                "id": aluno.id,
                "nome": aluno.nome,
                "serie": aluno.serie,
                "turma": aluno.turma,
            }
        )

    return resultado
