from getpass import getpass

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError

from gestao.models import Administrador


class Command(BaseCommand):
    help = "Cria ou atualiza um administrador com senha protegida por hash."

    def add_arguments(self, parser):
        parser.add_argument("--nome", required=True)
        parser.add_argument("--usuario", required=True)

    def handle(self, *args, **options):
        senha = getpass("Senha: ")
        confirmacao = getpass("Confirme a senha: ")
        if not senha:
            raise CommandError("A senha não pode ficar vazia.")
        if senha != confirmacao:
            raise CommandError("As senhas não coincidem.")

        administrador, criado = Administrador.objects.using("admin_db").update_or_create(
            usuario=options["usuario"].strip(),
            defaults={
                "nome": options["nome"].strip(),
                "senha": make_password(senha),
            },
        )
        acao = "criado" if criado else "atualizado"
        self.stdout.write(
            self.style.SUCCESS(f"Administrador {administrador.usuario} {acao}.")
        )
