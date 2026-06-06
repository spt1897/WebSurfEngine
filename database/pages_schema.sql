create database if not exists WebSurfDB;
use WebSurfDB;

create table if not exists WebPages (
    id int AUTO_INCREMENT primary key,
    url varchar(768) not null unique,
    title varchar(3000),
    description text,
    favicon varchar(3000),
    domain varchar(100) not null,
    scheme varchar(10) not null,
    popul_score float default 0.0,
    cred_score float default 0.0,
    last_crawled timestamps,
    index index_domain (domain)
);

create table if not exists keywords(
    id int AUTO_INCREMENT primary key,
    keyword varchar(300) not null,
    page_id int not null,
    tf int default 1,
    foreign key(page_id) references WebPages(id) on delete cascade,
    index index_keyword (keyword),
    index index_page_id (page_id),
    unique(keyword,page_id)
);

