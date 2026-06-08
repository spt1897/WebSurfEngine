create database if not exists WebSurfDB;
use WebSurfDB;

create table if not exists pagemap(
    source_url varchar(768) not null,
    destination_url varchar(768) not null,
    
);