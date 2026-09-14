from django.urls import path

from .views import colecao_alunos, progressao_anual


urlpatterns = [
    path("", colecao_alunos, name="alunos"),
    path("progredir/", progressao_anual, name="progressao-anual"),
]
