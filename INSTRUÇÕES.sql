

-- INSTRUÇÕES CASO QUEIRA FAZER ALGUMA MODIFICAÇÃO NO BD OU FAZER TESTES E DECIDIR APAGAR DPS --

 
-- desativar verificacao de foreign keys
set foreign_key_checks = 0;

-- limpar emprestimos
use livros;
truncate table emprestimos;

-- limpar catalogo de livros
truncate table catalogo_livros;

-- limpar administradores
use admin;
truncate table administradores;

-- limpar alunos
use usuarios;
truncate table alunos;

-- reativar verificacao de foreign keys
set foreign_key_checks = 1;
