-- maketables.sql sets up the tables for wendi_db

use wendi_db;

DROP TABLE IF EXISTS `media`;
DROP TABLE IF EXISTS `collectionEntry`;
DROP TABLE IF EXISTS `collection`;
DROP TABLE IF EXISTS `comment`;
DROP TABLE IF EXISTS `review`;
DROP TABLE IF EXISTS `room`;
DROP TABLE IF EXISTS `hall`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `username` VARCHAR(12) NOT NULL PRIMARY KEY,
  `email` VARCHAR(50) NOT NULL,
  `classYear` CHAR(4) NOT NULL,
  `numReview` INT NOT NULL
)
ENGINE = InnoDB;

CREATE TABLE `hall` (
  `id` CHAR(3) PRIMARY KEY,
  `name` VARCHAR(20),
  `complex` VARCHAR(30),
  `mediaFilepath` VARCHAR(255),
  `toQuad` INT,
  `toGym` INT,
  `toDining` INT,
  `toSci` INT,
  `toShuttle` INT,
  `toLulu` INT,
  `toParking` INT
)
ENGINE = InnoDB;

CREATE TABLE `room` (
  `id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `number` CHAR(10),
  `hid` CHAR(3),
  `type` ENUM ('First Year', 'Upperclass', 'Residential Staff', 'Academic Success Coach'),
  `description` VARCHAR(30),
  `numReviews` INT,
  FOREIGN KEY (hid) REFERENCES hall(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
ENGINE = InnoDB;

CREATE TABLE `review` (
  `id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `uid` INT,
  `rid` INT,
  `rating` INT,
  `startTime` DATE,
  `lengthOfStay` ENUM ('Winter', 'Summer', 'Spring Only', 'Fall Only', 'Whole Year'),
  `sizeScore` FLOAT,
  `storageScore` FLOAT,
  `ventScore` FLOAT,
  `cleanScore` FLOAT,
  `bathroomScore` FLOAT,
  `accessibilityScore` FLOAT,
  `sunlightScore` FLOAT,
  `bugScore` FLOAT,
  `windowScore` FLOAT,
  `noiseScore` FLOAT,
  `comment` VARCHAR(3000),
  `hasMedia` BOOLEAN,
  `timePosted` TIMESTAMP,
  FOREIGN KEY (`uid`) REFERENCES `userpass`(`uid`)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,  
  FOREIGN KEY (`rid`) REFERENCES `room`(`id`)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
ENGINE = InnoDB;

CREATE TABLE `comment` (
  `id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `uid` INT,
  `rid` INT,
  `content` VARCHAR(1500),
  `hasMedia` BOOLEAN,
  `timePosted` timestamp,
  FOREIGN KEY (uid) REFERENCES `userpass`(`uid`)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
  FOREIGN KEY (rid) REFERENCES room(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
ENGINE = InnoDB;

CREATE TABLE `collection` (
  `id` INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `uid` INT,
  `name` VARCHAR(50),
  FOREIGN KEY (uid) REFERENCES `userpass`(`uid`)
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
  `url` VARCHAR(200),
  `uid` INT,
  `rid` INT,
  `cid` INT,
  FOREIGN KEY (uid) REFERENCES `userpass`(`uid`)
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
