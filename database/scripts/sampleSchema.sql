
create database testdb1;
use testdb1;

create table table1(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col1)
);
create table table2(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col1)
);
create table table3(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col2)
);
create table table4(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col2)
);
ALTER TABLE table3
ADD FOREIGN KEY (col1) REFERENCES table2(col1);

ALTER TABLE table1
ADD FOREIGN KEY (col2) REFERENCES table4(col2);

ALTER TABLE table2
ADD FOREIGN KEY (col2) REFERENCES table4(col2);


create database testdb2;
use testdb2;

create table table1(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col1)
);
create table table2(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col1)
);
create table table3(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col2)
);
create table table4(
	col1 varchar(30) ,
    col2 varchar(30),
    primary key(col2)
);
ALTER TABLE table3
ADD FOREIGN KEY (col1) REFERENCES table2(col1);

ALTER TABLE table1
ADD FOREIGN KEY (col2) REFERENCES table4(col2);

ALTER TABLE table2
ADD FOREIGN KEY (col2) REFERENCES table4(col2);



