-- Emma Lim
-- contacts.sql sets up the tables

use el110_db;

drop table if exists phonenums;
drop table if exists addresses;
drop table if exists uniqueppl;


create table uniqueppl (
    pid int NOT NULL,
    name varchar(30),
    primary key (pid),
    index (pid)
)
ENGINE = InnoDB;

create table addresses (
    pid int NOT NULL,                                                                                                                                                     
    name varchar(30),
    kind varchar(10),
    city varchar(30),
    state char(2),
    index (pid),
    foreign key (pid) references uniqueppl(pid)
        on update restrict
        on delete cascade
)
ENGINE = InnoDB;


create table phonenums (
    pid int NOT NULL,
    name varchar(30),
    kind varchar(10),
    phnum varchar(12),
    index (pid),
    foreign key (pid) references uniqueppl(pid)
        on update restrict
        on delete cascade
)
ENGINE = InnoDB;
