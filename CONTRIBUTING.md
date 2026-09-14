# Como contribuir

A branch `main` deve permanecer estável.

1. Atualize a `main` e crie uma branch curta: `feature/nome`, `fix/nome` ou `docs/nome`.
2. Trabalhe em uma responsabilidade pequena.
3. Execute os testes descritos no README.
4. Abra um Pull Request explicando o que mudou e como testar.
5. Outra pessoa revisa antes do merge.

## Organização do grupo

Ninguém precisa ficar preso para sempre a uma área. A cada tarefa, registrem no Project quem implementa e quem revisa.

- Coordenação/integração: acompanha branches, PRs e comunicação entre as partes.
- Backend Django: URLs, views, autenticação, serviços e regras de negócio.
- Banco de dados: schemas, integridade, consultas e apoio aos modelos Django.
- Frontend: telas e integração com a API.
- Testes/documentação: valida os fluxos e mantém instruções atualizadas.

## Regras importantes

- Nunca faça commit de `.env`, senha ou dados reais de alunos.
- Dados de demonstração devem ser fictícios.
- Não altere os três schemas sem atualizar `docs/ARQUITETURA.md`.
- Não use `force push` na `main`.
- Mudanças de banco precisam de backup e revisão.
