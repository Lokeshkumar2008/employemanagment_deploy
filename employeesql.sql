create database company;
use company;

create table users (
id int primary key auto_increment,
username varchar(40),
password varchar(40),
email varchar(50),
role varchar(20)
);

create table employee(
eid int primary key auto_increment,
ename varchar(50),
edept varchar(50),
email varchar(50),
esalary int,
ephone varchar(15)
);
insert into users ( username,password,role) values
('lokesh', "loki","hr");
insert into employee (ename,edept,esalary,ephone) values
("mahe", 'bca',25000,1234567890);