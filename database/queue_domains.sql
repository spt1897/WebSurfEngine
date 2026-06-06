create database if not exists WebSurfDB;
use WebSurfDB;

create table if not exists crawl_queue(
    id int AUTO_INCREMENT primary key,
    url varchar(768) not null unique,
    status enum("not_crawled","in_process","crawled") not null
    in_process_started timestamps default null
);

create table if not exists domains(
    domain varchar(100) not null unique,
    num_pages int default 0
);