create database if not exists WebSurfDB;
use WebSurfDB;

create table if not exists WebPages (
    id int AUTO_INCREMENT primary key,
    url varchar(768) not null unique,
    title varchar(3000),
    description text,
    favicon varchar(3000),
    domain varchar(100) not null,
    popul_score float default 0.0,
    cred_score float default 0.0
);

create table if not exists keywords(
    id int AUTO_INCREMENT primary key,
    keyword varchar(300) not null,
    page_id int not null,
    wordfreq int default 1,
    tf_idf float default 0.0,
    foreign key(page_id) references WebPages(id) on delete cascade,
    index index_keyword (keyword),
    index index_page_id (page_id)

);

create table if not exists url_queue(
    url varchar(768) not null unique,
    status enum("not_crawled","in_process","crawled") not null
);

create table if not exists domains(
    domain varchar(100) not null unique,
    num_pages int default 0
);