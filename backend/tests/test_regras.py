import unittest

from acervo.domain import (
    estoque_apos_devolucao,
    estoque_apos_emprestimo,
    validar_devolucao,
)
from alunos.domain import calcular_proxima_serie


class ProgressaoTests(unittest.TestCase):
    def test_promove_primeiro_e_segundo_ano(self):
        self.assertEqual(calcular_proxima_serie(1), 2)
        self.assertEqual(calcular_proxima_serie(2), 3)

    def test_terceiro_ano_conclui(self):
        self.assertIsNone(calcular_proxima_serie(3))

    def test_rejeita_serie_invalida(self):
        with self.assertRaises(ValueError):
            calcular_proxima_serie(4)


class EstoqueTests(unittest.TestCase):
    def test_emprestimo_reduz_disponibilidade(self):
        self.assertEqual(estoque_apos_emprestimo(3, 2), 1)

    def test_nao_empresta_sem_exemplar(self):
        with self.assertRaises(ValueError):
            estoque_apos_emprestimo(3, 0)

    def test_devolucao_recompoe_disponibilidade(self):
        self.assertEqual(estoque_apos_devolucao(3, 2), 3)

    def test_nao_devolve_duas_vezes(self):
        with self.assertRaises(ValueError):
            validar_devolucao("devolvido")


if __name__ == "__main__":
    unittest.main()
