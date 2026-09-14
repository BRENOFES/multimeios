CREATE DATABASE IF NOT EXISTS livros
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE livros;

CREATE TABLE IF NOT EXISTS catalogo_livros (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  autor VARCHAR(150) NOT NULL,
  editora VARCHAR(100),
  categoria VARCHAR(50),
  quantidade_total INT UNSIGNED NOT NULL DEFAULT 1,
  quantidade_disponivel INT UNSIGNED NOT NULL DEFAULT 1,
  localizacao VARCHAR(50),
  criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_livros_total CHECK (quantidade_total > 0),
  CONSTRAINT chk_livros_disponivel
    CHECK (quantidade_disponivel <= quantidade_total)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS emprestimos (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT UNSIGNED NULL,
  admin_id INT UNSIGNED NOT NULL,
  livro_id INT UNSIGNED NOT NULL,
  aluno_nome VARCHAR(100) NOT NULL,
  data_aluguel DATE NOT NULL,
  data_prevista DATE NOT NULL,
  data_recebimento DATE NULL,
  status ENUM('alugado', 'devolvido', 'atrasado') NOT NULL DEFAULT 'alugado',
  criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_emprestimos_usuario (usuario_id),
  INDEX idx_emprestimos_admin (admin_id),
  INDEX idx_emprestimos_livro_status (livro_id, status),
  CONSTRAINT fk_emprestimos_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuarios.alunos(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_emprestimos_admin
    FOREIGN KEY (admin_id) REFERENCES admin.administradores(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_emprestimos_livro
    FOREIGN KEY (livro_id) REFERENCES catalogo_livros(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;
