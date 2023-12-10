use wendi_db;

create table userpass(
      uid int auto_increment,
      username varchar(50) not null,
      email varchar(50) not null,
      classYear char(4) not null,
      hashed char(60),
      unique(username),
      index(username),
      primary key (uid)
)
ENGINE = InnoDB;