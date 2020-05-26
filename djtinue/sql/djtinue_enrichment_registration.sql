CREATE TABLE IF NOT EXISTS `djtinue_enrichment_registration` (
  `contact_ptr_id` int(11) NOT NULL,
  `phone_home` varchar(12) NOT NULL,
  `phone_work` varchar(12) DEFAULT NULL,
  `email_work` varchar(128) DEFAULT NULL,
  `date_of_birth` date NOT NULL,
  `social_security_number` varchar(255) DEFAULT NULL,
  `social_security_four` varchar(4) DEFAULT NULL,
  `attended_before` varchar(3) NOT NULL,
  `collegeid` varchar(8) DEFAULT NULL,
  `verify` tinyint(1) NOT NULL,
  PRIMARY KEY (`contact_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
