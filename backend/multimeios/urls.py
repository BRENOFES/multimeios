from django.urls import include, path

from .views import saude


urlpatterns = [
    path("api/saude/", saude, name="saude"),
    path("api/admin/", include("gestao.urls")),
    path("api/alunos/", include("alunos.urls")),
    path("api/acervo/", include("acervo.urls")),
]
