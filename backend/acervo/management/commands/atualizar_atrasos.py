from django.core.management.base import BaseCommand

from acervo.services import atualizar_emprestimos_atrasados


class Command(BaseCommand):
    help = "Marca como atrasados os empréstimos cuja data prevista já passou."

    def handle(self, *args, **options):
        quantidade = atualizar_emprestimos_atrasados()
        self.stdout.write(
            self.style.SUCCESS(f"{quantidade} empréstimo(s) atualizado(s).")
        )
