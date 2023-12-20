USE wendi_db;

CREATE TABLE userpass (
    uid INT AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    classYear CHAR(4) NOT NULL,
    hashed CHAR(60) NOT NULL,
    UNIQUE (username),
    INDEX (username),
    PRIMARY KEY (uid)
)
ENGINE = InnoDB;
