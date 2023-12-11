-- maketables.sql sets up the tables for wendi_db

use wendi_db;

DROP TABLE IF EXISTS `media`;
DROP TABLE IF EXISTS `collectionEntry`;
DROP TABLE IF EXISTS `collection`;
DROP TABLE IF EXISTS `comment`;

CREATE TABLE `comment` (
  `id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `uid` VARCHAR(12),
  `rid` INT,
  `content` VARCHAR(1500),
  `hasMedia` BOOLEAN,
  `timePosted` timestamp,
  FOREIGN KEY (uid) REFERENCES userpass(username)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
  FOREIGN KEY (rid) REFERENCES room(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
ENGINE = InnoDB;

CREATE TABLE `collection` (
  `id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `uid` VARCHAR(12),
  `name` VARCHAR(50),
  FOREIGN KEY (uid) REFERENCES `userpass`(`username`)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
ENGINE = InnoDB;

CREATE TABLE `collectionEntry` (
  `cid` INT,
  `rid` INT,
  FOREIGN KEY (cid) REFERENCES collection(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
  FOREIGN KEY (rid) REFERENCES room(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
ENGINE = InnoDB;

CREATE TABLE `media` (
  `id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `url` VARCHAR(255),
  `uid` VARCHAR(12),
  `rid` INT,
  `cid` INT,
  FOREIGN KEY (uid) REFERENCES `userpass`(`username`)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
  FOREIGN KEY (rid) REFERENCES review(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
  FOREIGN KEY (cid) REFERENCES comment(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
ENGINE = InnoDB;