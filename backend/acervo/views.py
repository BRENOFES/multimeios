import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from gestao.auth import obter_admin_da_requisicao, requer_admin
from .models import Emprestimo, Livro
from .services import RegraEmprestimo, criar_emprestimo, devolver_emprestimo


def _json(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError("JSON inválido.") from exc


def _livro_json(livro):
    return {
        "id": livro.id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "editora": livro.editora,
        "categoria": livro.categoria,
        "quantidade_total": livro.quantidade_total,
        "quantidade_disponivel": livro.quantidade_disponivel,
        "disponivel": livro.quantidade_disponivel > 0,
        "localizacao": livro.localizacao,
    }


def _emprestimo_json(emprestimo):
    return {
        "id": emprestimo.id,
        "usuario_id": emprestimo.usuario_id,
        "aluno_nome": emprestimo.aluno_nome,
        "admin_id": emprestimo.admin_id,
        "livro": _livro_json(emprestimo.livro),
        "data_aluguel": emprestimo.data_aluguel.isoformat(),
        "data_prevista": emprestimo.data_prevista.isoformat(),
        "data_recebimento": (
            emprestimo.data_recebimento.isoformat()
            if emprestimo.data_recebimento
            else None
        ),
        "status": emprestimo.status,
    }


@require_http_methods(["GET", "POST"])
def livros(request):
    if request.method == "GET":
        itens = Livro.objects.using("default").all()
        return JsonResponse({"livros": [_livro_json(item) for item in itens]})

    administrador = obter_admin_da_requisicao(request)
    if administrador is None:
        return JsonResponse(
            {"erro": "Autenticação administrativa necessária."},
            status=401,
        )

    try:
        dados = _json(request)
        quantidade_total = int(dados.get("quantidade_total", 1))
        quantidade_disponivel = int(
            dados.get("quantidade_disponivel", quantidade_total)
        )
        livro = Livro(
            titulo=str(dados["titulo"]).strip(),
            autor=str(dados["autor"]).strip(),
            editora=str(dados.get("editora") or "").strip() or None,
            categoria=str(dados.get("categoria") or "").strip() or None,
            quantidade_total=quantidade_total,
            quantidade_disponivel=quantidade_disponivel,
            localizacao=str(dados.get("localizacao") or "").strip() or None,
        )
        livro.full_clean()
        livro.save(using="default")
    except KeyError as exc:
        return JsonResponse(
            {"erro": f"Campo obrigatório ausente: {exc.args[0]}."}, status=400
        )
    except (TypeError, ValueError, ValidationError) as exc:
        mensagem = getattr(exc, "message_dict", None) or str(exc)
        return JsonResponse({"erro": mensagem}, status=400)

    return JsonResponse({"livro": _livro_json(livro)}, status=201)


@require_http_methods(["GET", "POST"])
@requer_admin
def emprestimos(request):
    if request.method == "GET":
        itens = (
            Emprestimo.objects.using("default")
            .select_related("livro")
            .all()
        )
        return JsonResponse(
            {"emprestimos": [_emprestimo_json(item) for item in itens]}
        )

    try:
        dados = _json(request)
        emprestimo = criar_emprestimo(
            usuario_id=int(dados["usuario_id"]),
            admin_id=request.administrador.id,
            livro_id=int(dados["livro_id"]),
            prazo_dias=dados.get("prazo_dias", 7),
        )
        emprestimo = (
            Emprestimo.objects.using("default")
            .select_related("livro")
            .get(pk=emprestimo.id)
        )
    except KeyError as exc:
        return JsonResponse(
            {"erro": f"Campo obrigatório ausente: {exc.args[0]}."}, status=400
        )
    except (TypeError, ValueError, RegraEmprestimo) as exc:
        return JsonResponse({"erro": str(exc)}, status=400)

    return JsonResponse(
        {"emprestimo": _emprestimo_json(emprestimo)},
        status=201,
    )


@require_POST
@requer_admin
def devolver(request, emprestimo_id):
    try:
        emprestimo = devolver_emprestimo(emprestimo_id=emprestimo_id)
        emprestimo = (
            Emprestimo.objects.using("default")
            .select_related("livro")
            .get(pk=emprestimo.id)
        )
    except RegraEmprestimo as exc:
        return JsonResponse({"erro": str(exc)}, status=400)

    return JsonResponse({"emprestimo": _emprestimo_json(emprestimo)})
