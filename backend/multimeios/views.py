from django.db import connections
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def saude(request):
    bancos = {}
    for alias in ("usuarios", "admin_db", "default"):
        try:
            with connections[alias].cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            bancos[alias] = "ok"
        except Exception:
            bancos[alias] = "indisponível"

    status = 200 if all(valor == "ok" for valor in bancos.values()) else 503
    return JsonResponse({"sistema": "multimeios", "bancos": bancos}, status=status)
