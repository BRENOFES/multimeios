import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from gestao.auth import requer_admin
from .models import Aluno
from .services import progredir_alunos


def _json(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError("JSON inválido.") from exc


def _aluno_json(aluno):
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "serie": aluno.serie,
        "turma": aluno.turma,
        "curso": aluno.curso,
        "criado_em": aluno.criado_em.isoformat() if aluno.criado_em else None,
    }


@require_http_methods(["GET", "POST"])
@requer_admin
def colecao_alunos(request):
    if request.method == "GET":
        alunos = Aluno.objects.using("usuarios").all()
        return JsonResponse({"alunos": [_aluno_json(item) for item in alunos]})

    try:
        dados = _json(request)
        aluno = Aluno(
            nome=str(dados["nome"]).strip(),
            serie=int(dados["serie"]),
            turma=str(dados["turma"]).strip(),
            curso=str(dados["curso"]).strip(),
        )
        aluno.full_clean()
        aluno.save(using="usuarios")
    except KeyError as exc:
        return JsonResponse(
            {"erro": f"Campo obrigatório ausente: {exc.args[0]}."}, status=400
        )
    except (TypeError, ValueError, ValidationError) as exc:
        mensagem = getattr(exc, "message_dict", None) or str(exc)
        return JsonResponse({"erro": mensagem}, status=400)

    return JsonResponse({"aluno": _aluno_json(aluno)}, status=201)


@require_POST
@requer_admin
def progressao_anual(request):
    try:
        dados = _json(request)
        turmas = dados.get("turmas_por_aluno", {})
        if not isinstance(turmas, dict):
            raise ValueError("turmas_por_aluno precisa ser um objeto JSON.")
        resultado = progredir_alunos(turmas)
    except (ValueError, ValidationError) as exc:
        mensagem = getattr(exc, "message_dict", None) or str(exc)
        return JsonResponse({"erro": mensagem}, status=400)

    return JsonResponse(resultado)
