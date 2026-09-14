from django.core.validators import MinValueValidator
from django.db import models


class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    editora = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    quantidade_total = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    quantidade_disponivel = models.PositiveIntegerField(default=1)
    localizacao = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "acervo"
        db_table = "catalogo_livros"
        managed = False
        ordering = ["titulo"]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.quantidade_disponivel > self.quantidade_total:
            raise ValidationError(
                {"quantidade_disponivel": "Não pode superar a quantidade total."}
            )

    def __str__(self):
        return self.titulo


class Emprestimo(models.Model):
    class Status(models.TextChoices):
        ALUGADO = "alugado", "Alugado"
        DEVOLVIDO = "devolvido", "Devolvido"
        ATRASADO = "atrasado", "Atrasado"

    usuario_id = models.PositiveIntegerField(null=True, blank=True)
    admin_id = models.PositiveIntegerField()
    livro = models.ForeignKey(
        Livro,
        db_column="livro_id",
        on_delete=models.PROTECT,
        related_name="emprestimos",
    )
    aluno_nome = models.CharField(max_length=100)
    data_aluguel = models.DateField()
    data_prevista = models.DateField()
    data_recebimento = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ALUGADO,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "acervo"
        db_table = "emprestimos"
        managed = False
        ordering = ["-data_aluguel", "-id"]

    def __str__(self):
        return f"{self.aluno_nome} — {self.livro.titulo}"
