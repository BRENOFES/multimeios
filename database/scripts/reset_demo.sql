-- ATENÇÃO: remove todos os registros das tabelas do projeto.
-- Use somente no ambiente de desenvolvimento e depois de confirmar o backup.

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE livros.emprestimos;
TRUNCATE TABLE livros.catalogo_livros;
TRUNCATE TABLE admin.administradores;
TRUNCATE TABLE usuarios.alunos;

SET FOREIGN_KEY_CHECKS = 1;
