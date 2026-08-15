
CREATE DATABASE usuarios;
USE  usuarios;

 -- USUÁRIOS (ALUNOS) -- 


CREATE TABLE alunos (
id int auto_increment primary key,
nome varchar (90) not null,
serie int not null,
curso varchar (20) not null,
criado_em timestamp default current_timestamp
);

insert into alunos (id,nome,serie,curso) values
(1,'breno haniel',2, 'rdc');

select * from alunos

 

 