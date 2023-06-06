create database bookstore;

use bookstore;

create table book
(
    id          int auto_increment comment '主键ID' primary key,
    name        varchar(50)  default '' not null comment '书名',
    pic_url     varchar(255) default '' not null comment '图片外链',
    auther      varchar(20)             not null comment '作者',
    category    int                     not null comment '当前分类',
    source_id   int                     not null comment '来源ID',
    source_url  varchar(255)            not null comment '来源URL',
    create_date date                    not null comment '上线时间',
    update_time datetime                not null comment '最近更新时间'
)
    comment '图书表';

create table category
(
    id    int auto_increment  primary key,
    pid   int         not null comment '父ID',
    level int         not null comment '等级',
    name  varchar(50) not null comment '分类名称'
)
    comment '分类表';

create table source
(
    id          int auto_increment comment '主键' primary key,
    home        varchar(255)                       not null comment '主页地址',
    name        varchar(20)                        not null comment '资源名称',
    type        int                                not null comment '类别',
    create_time datetime default CURRENT_TIMESTAMP not null comment '创建时间'
)
    comment '资源表';

