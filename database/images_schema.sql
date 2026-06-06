create database if not exists WebSurfDB;
use WebSurfDB;

create table if not exists images(
    id int AUTO_INCREMENT primary key,
    page_id int not null,
    image_url varchar(768) not null unique,
    description text,
    foreign key(page_id) references WebPages(id) on delete cascade
    index index_page_id(page_id)
);

create table if not exists image_index(
    id int AUTO_INCREMENT primary key,
    image_id int not null,
    keyword varchar(300) not null,
    tf int default 1,
    foreign key (image_id) references images(id) on delete cascade,
    index index_keyword (keyword),
    index index_image_id (image_id),
    unique(image_id,keyword)
);