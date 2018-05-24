# Host: 192.168.200.128  (Version 5.7.22-0ubuntu18.04.1)
# Date: 2018-05-24 22:55:27
# Generator: MySQL-Front 6.0  (Build 2.20)


#
# Structure for table "cast"
#

DROP TABLE IF EXISTS `cast`;
CREATE TABLE `cast` (
  `id` varchar(64) NOT NULL DEFAULT '',
  `url` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

#
# Data for table "cast"
#


#
# Structure for table "detail"
#

DROP TABLE IF EXISTS `detail`;
CREATE TABLE `detail` (
  `id` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `length` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

#
# Data for table "detail"
#


#
# Structure for table "detailroute"
#

DROP TABLE IF EXISTS `detailroute`;
CREATE TABLE `detailroute` (
  `num` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id` varchar(16) NOT NULL DEFAULT '',
  `tkey` varchar(16) NOT NULL DEFAULT '',
  `fkey` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#
# Data for table "detailroute"
#


#
# Structure for table "label"
#

DROP TABLE IF EXISTS `label`;
CREATE TABLE `label` (
  `id` varchar(64) NOT NULL DEFAULT '',
  `url` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

#
# Data for table "label"
#


#
# Structure for table "maker"
#

DROP TABLE IF EXISTS `maker`;
CREATE TABLE `maker` (
  `id` varchar(64) NOT NULL DEFAULT '',
  `url` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#
# Data for table "maker"
#

