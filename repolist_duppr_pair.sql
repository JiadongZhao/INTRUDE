-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: repolist
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `duppr_pair`
--

DROP TABLE IF EXISTS `duppr_pair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `duppr_pair` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `repo` varchar(50) NOT NULL,
  `pr1` varchar(25) NOT NULL,
  `pr2` varchar(25) NOT NULL,
  `score` decimal(16,15) DEFAULT NULL,
  `title` decimal(3,2) DEFAULT NULL,
  `description` decimal(3,2) DEFAULT NULL,
  `patch_content` decimal(3,2) DEFAULT NULL,
  `patch_content_overlap` decimal(3,2) DEFAULT NULL,
  `changed_file` decimal(3,2) DEFAULT NULL,
  `changed_file_overlap` decimal(4,2) DEFAULT NULL,
  `location` decimal(3,2) DEFAULT NULL,
  `location_overlap` decimal(3,2) DEFAULT NULL,
  `issue_number` decimal(3,2) DEFAULT NULL,
  `commit_message` decimal(3,2) DEFAULT NULL,
  `comment_sent` int(11) DEFAULT '0' COMMENT '0 - no action yet     1 - send comment    -1 - don''t send comment',
  `notes` blob,
  `link_clicked` int(11) DEFAULT '0' COMMENT '0 - link not clicked   1 - useful/dup clicked   2 - useful/not-dup clicked   3 - not-useful/not-dup clicked    4 - not-useful/other clicked',
  `comment_left` blob COMMENT 'contains comment if any is left',
  `repoID` int(11) DEFAULT NULL,
  `toppair` int(11) NOT NULL DEFAULT '0' COMMENT '0: default value, not top pair.  1: top pair by timestamp.  2: a comment has been sent to this repo (but not to this pair). -1: this pair was manually selected as top.',
  `timestamp` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1820 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-31 11:07:13
