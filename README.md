# Sistema Multimeios — EEEP Presidente Roosevelt

Sistema web para digitalizar o cadastro de alunos, o catálogo, a disponibilidade dos livros e os fluxos de empréstimo e devolução do Multimeios.

## Estrutura

- `backend/`: API Django e regras de negócio.
- `database/schema/`: criação dos três bancos MySQL.
- `database/seeds/`: dados fictícios para demonstração.
- `database/scripts/`: rotinas de manutenção dos dados de teste.
- `docs/`: decisões técnicas e fluxo de trabalho do grupo.

## Bancos mantidos

| Alias no Django | Banco MySQL | Responsabilidade |
|---|---|---|
| `usuarios` | `usuarios` | alunos, série e turma |
| `admin_db` | `admin` | administradores e senhas com hash |
| `default` | `livros` | catálogo, estoque e empréstimos |

Os três bancos ficam no mesmo servidor MySQL. O MySQL mantém as chaves estrangeiras entre schemas; o Django usa roteadores e valida IDs na camada de serviço porque o ORM não oferece relações entre bancos distintos.

## Executar localmente

Pré-requisitos: Python 3.12+, MySQL 8 e, opcionalmente, Docker.

```bash
docker compose up -d mysql
cd backend
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py criar_admin --nome "Equipe Multimeios" --usuario admin
python manage.py runserver
```

No Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py criar_admin --nome "Equipe Multimeios" --usuario admin
python manage.py runserver
```

O comando `criar_admin` pede a senha sem exibi-la e salva somente o hash.

## API inicial

- `GET /api/saude/`: verifica a conexão com os três bancos.
- `POST /api/admin/login/`: autentica um administrador e devolve um token temporário.
- `GET /api/acervo/livros/`: catálogo e disponibilidade.
- `POST /api/acervo/livros/`: cadastra livro (admin).
- `GET|POST /api/alunos/`: lista/cadastra alunos (admin).
- `POST /api/alunos/progredir/`: promove 1º→2º e 2º→3º; concluintes do 3º são removidos se não tiverem empréstimo ativo.
- `GET|POST /api/acervo/emprestimos/`: lista/cria empréstimos (admin).
- `POST /api/acervo/emprestimos/<id>/devolver/`: registra devolução (admin).

Nas rotas administrativas, envie `Authorization: Bearer <token>`.

## Testes

```bash
cd backend
python -m compileall .
python -m unittest discover -s tests
python manage.py check
```

Leia [docs/ARQUITETURA.md](docs/ARQUITETURA.md) antes de alterar modelos ou bancos e [CONTRIBUTING.md](CONTRIBUTING.md) antes de enviar código.
