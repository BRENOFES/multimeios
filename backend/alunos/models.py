from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    serie = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    turma = models.CharField(max_length=20)
    curso = models.CharField(max_length=50)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "alunos"
        db_table = "alunos"
        managed = False
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} — {self.serie}º {self.turma}"
