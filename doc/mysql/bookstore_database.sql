create database bookstore;

use bookstore;

create table bookstore.book
(
    id                       int auto_increment comment '主键ID'
        primary key,
    name                     varchar(50)  default ''   not null comment '书名',
    pic_url                  varchar(255) default ''   not null comment '图片外链',
    auther                   varchar(20)  default ''   not null comment '作者',
    category                 int          default 0    not null comment '当前分类',
    source_id                int          default 1    not null comment '来源ID',
    source_url               varchar(255)              not null comment '来源URL',
    last_update_chapter_name varchar(50)               null comment '最后更新的章节名称',
    create_date              date                      not null comment '上线时间',
    update_time              datetime                  null on update CURRENT_TIMESTAMP comment '最近更新时间',
    end_flag                 bit          default b'0' not null comment '结束状态',
    status                   int          default 0    not null comment '状态 0未获取 1待更新'
)
    comment '图书表';







create table bookstore.category
(
    id    int auto_increment  primary key,
    pid   int         not null comment '父ID',
    level int         not null comment '等级',
    name  varchar(50) not null comment '分类名称'
)
    comment '分类表';

create table bookstore.source
(
    id          int auto_increment comment '主键' primary key,
    home        varchar(255)                       not null comment '主页地址',
    name        varchar(20)                        not null comment '资源名称',
    type        int                                not null comment '类别',
    create_time datetime default CURRENT_TIMESTAMP not null comment '创建时间'
)
    comment '资源表';

