from django.contrib.auth.hashers import check_password
from django.db import models


class Administrador(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "gestao"
        db_table = "administradores"
        managed = False
        ordering = ["nome"]

    def senha_confere(self, senha_pura):
        return check_password(senha_pura, self.senha)

    def __str__(self):
        return self.nome
