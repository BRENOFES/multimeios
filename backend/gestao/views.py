import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .auth import emitir_token
from .models import Administrador


@require_POST
def login(request):
    try:
        dados = json.loads(request.body or "{}")
        usuario = str(dados["usuario"]).strip()
        senha = str(dados["senha"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return JsonResponse({"erro": "Informe usuário e senha em JSON."}, status=400)

    administrador = (
        Administrador.objects.using("admin_db").filter(usuario=usuario).first()
    )
    if administrador is None or not administrador.senha_confere(senha):
        return JsonResponse({"erro": "Credenciais inválidas."}, status=401)

    return JsonResponse(
        {
            "token": emitir_token(administrador),
            "expira_em_segundos": 8 * 60 * 60,
            "administrador": {
                "id": administrador.id,
                "nome": administrador.nome,
                "usuario": administrador.usuario,
            },
        }
    )
