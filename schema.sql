create extension if not exists "uuid-ossp";
drop table if exists users;
create table if not exists users (
       username varchar(16) NOT NULL,
       password varchar(16) NOT NULL,
       id uuid NOT NULL DEFAULT uuid_generate_v4()
);

insert into users (username, password) values ('test1', 'testpassword1');
insert into users (username, password) values ('test2', 'testpassword2');
