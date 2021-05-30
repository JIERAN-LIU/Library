create database library character set utf8mb4;
create user 'library'@'%' identified by 'Library_12345678';
grant all privileges on library.* to 'library'@'%';
flush privileges;