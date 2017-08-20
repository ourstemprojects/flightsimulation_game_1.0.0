-- Adminer 3.3.3 MySQL dump

SET NAMES utf8;
SET foreign_key_checks = 0;
SET time_zone = 'SYSTEM';
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `avatardata`;
CREATE TABLE `avatardata` (
  `rownum` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `status` varchar(8) NOT NULL,
  `datecreated` datetime NOT NULL,
  `gamehighscore` bigint(20) unsigned NOT NULL,
  `queueposition` bigint(20) unsigned NOT NULL,
  `avatar` longblob NOT NULL,
  `completiontime` bigint(20) NOT NULL,
  PRIMARY KEY (`rownum`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `gamedata`;
CREATE TABLE `gamedata` (
  `rownum` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `actualprofiledata` longblob NOT NULL,
  `targetprofiledata` longblob NOT NULL,
  `gamehighscore` bigint(20) unsigned NOT NULL,
  `completiontime` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`rownum`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


-- 2017-08-05 21:30:04

