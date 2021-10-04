DROP TABLE IF EXISTS `djtinue_course`;
CREATE TABLE `djtinue_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `course_number` varchar(128) NOT NULL,
  `abstract` longtext NOT NULL,
  `credits` varchar(8) NOT NULL,
  `audience` varchar(128) NOT NULL,
  `fac_id` varchar(16) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `instructors` varchar(512) DEFAULT NULL,
  `dates` varchar(255) DEFAULT NULL,
  `room` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
