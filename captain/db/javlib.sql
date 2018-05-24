# Host: localhost  (Version: 5.5.53)
# Date: 2018-05-24 08:08:19
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

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
  `maker` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cast` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `maker` (`maker`),
  KEY `label` (`label`),
  FULLTEXT KEY `title` (`title`),
  FULLTEXT KEY `cast` (`cast`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

#
# Data for table "detail"
#

/*!40000 ALTER TABLE `detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `detail` ENABLE KEYS */;
