create database if not exists WebSurfDB;
use WebSurfDB;

create table if not exists df(
    keyword varchar(300) not null,
    df int not null
);