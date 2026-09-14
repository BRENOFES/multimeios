INSERT INTO usuarios.alunos (nome, serie, turma, curso) VALUES
  ('Ana Souza', 1, '1A', 'Redes de Computadores'),
  ('Carlos Lima', 2, '2B', 'Informática'),
  ('Marina Alves', 3, '3A', 'Administração');

INSERT INTO livros.catalogo_livros
  (titulo, autor, editora, categoria, quantidade_total, quantidade_disponivel, localizacao)
VALUES
  ('Capitães da Areia', 'Jorge Amado', 'Companhia das Letras', 'Literatura brasileira', 3, 3, 'A-01'),
  ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 'Agir', 'Literatura', 2, 2, 'A-02'),
  ('Redes de Computadores', 'Andrew S. Tanenbaum', 'Pearson', 'Tecnologia', 1, 1, 'T-01');
