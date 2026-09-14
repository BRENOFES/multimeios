# Arquitetura do banco e do backend

## Visão geral

O projeto mantém três bancos MySQL no mesmo servidor:

- `usuarios`: tabela `alunos`.
- `admin`: tabela `administradores`.
- `livros`: tabelas `catalogo_livros` e `emprestimos`.

O Django configura três conexões e o arquivo `multimeios/db_router.py` envia cada app ao banco correto.

## Decisão sobre relações entre bancos

O ORM do Django não garante chaves estrangeiras entre bancos diferentes. Por isso:

- `Emprestimo.livro` é uma relação Django normal, pois ambos estão em `livros`;
- `usuario_id` e `admin_id` são IDs simples no modelo Django;
- a camada `acervo/services.py` confirma que aluno e administrador existem antes do empréstimo;
- o MySQL continua com as FKs entre schemas, pois os três bancos usam a mesma instância.

Não transforme `usuario_id` ou `admin_id` em `ForeignKey` do Django enquanto os modelos estiverem em conexões diferentes.

## Progressão anual

- Aluno no 1º ano passa ao 2º.
- Aluno no 2º ano passa ao 3º.
- Aluno concluinte do 3º ano é removido.
- Um concluinte com empréstimo ativo fica bloqueado até devolver o livro.
- Ao remover um concluinte, empréstimos antigos preservam o nome registrado e recebem `usuario_id = NULL`.

A turma nova pode ser enviada por aluno na operação de progressão. Se não for enviada, a identificação atual da turma é mantida.

## Consistência

Empréstimo e devolução bloqueiam as linhas do livro com `SELECT ... FOR UPDATE`, evitando que dois atendimentos retirem o último exemplar ao mesmo tempo. A alteração de estoque e o registro do empréstimo acontecem na mesma transação do banco `livros`.

Não existe transação atômica única envolvendo os três bancos no Django. As consultas externas são validadas antes da transação de estoque, e as FKs do MySQL funcionam como proteção final.
