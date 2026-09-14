from functools import wraps

from django.core import signing
from django.http import JsonResponse

from .models import Administrador


TOKEN_SALT = "multimeios.admin"
TOKEN_DURACAO_SEGUNDOS = 8 * 60 * 60


def emitir_token(administrador):
    return signing.dumps(
        {"admin_id": administrador.id, "usuario": administrador.usuario},
        salt=TOKEN_SALT,
        compress=True,
    )


def obter_admin_da_requisicao(request):
    cabecalho = request.headers.get("Authorization", "")
    prefixo = "Bearer "
    if not cabecalho.startswith(prefixo):
        return None

    try:
        dados = signing.loads(
            cabecalho[len(prefixo):],
            salt=TOKEN_SALT,
            max_age=TOKEN_DURACAO_SEGUNDOS,
        )
        return Administrador.objects.using("admin_db").get(pk=dados["admin_id"])
    except (signing.BadSignature, signing.SignatureExpired, Administrador.DoesNotExist):
        return None


def requer_admin(view):
    @wraps(view)
    def protegida(request, *args, **kwargs):
        administrador = obter_admin_da_requisicao(request)
        if administrador is None:
            return JsonResponse(
                {"erro": "Autenticação administrativa necessária."},
                status=401,
            )
        request.administrador = administrador
        return view(request, *args, **kwargs)

    return protegida
