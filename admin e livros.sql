CREATE DATABASE IF NOT EXISTS livros;
Use livros;


create table catalogo_livros (
id int auto_increment primary key,
titulo varchar(150) not null,
autor varchar(150)not null,
editora varchar (100),
categoria varchar (50),
quantidade_total int default 1,
quantidade_disponivel int default 1, 

localizacao varchar(50),

criado_em timestamp default current_timestamp
);

-- PARA EMPRÉSTIMOS E DEVOLUÇÕES --

create table if not exists emprestimos (
id int auto_increment primary key,

usuario_id int not null,
admin_id int not null,
livro_id int not null,

data_aluguel date not null,
data_recebimento date,

status enum('alugado','devolvido', 'atrasado')
default 'alugado',

foreign key(usuario_id)
references usuarios.alunos(id),

foreign key (admin_id)
references   admin.administradores(id),

foreign key (livro_id)
references catalogo_livros(id)
);













create database if not exists admin;
use admin;

create table if not exists administradores (
id int auto_increment primary key,
nome varchar (100) not null,
usuario varchar(50) not null unique,
senha varchar (255) not null
);













 

 
 