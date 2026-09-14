from django.urls import path

from .views import devolver, emprestimos, livros


urlpatterns = [
    path("livros/", livros, name="livros"),
    path("emprestimos/", emprestimos, name="emprestimos"),
    path(
        "emprestimos/<int:emprestimo_id>/devolver/",
        devolver,
        name="devolver-emprestimo",
    ),
]
