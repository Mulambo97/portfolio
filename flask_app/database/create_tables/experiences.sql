CREATE TABLE IF NOT EXISTS `experiences` (
`experience_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identify each experience',
`position_id`   int(11) NOT NULL                  COMMENT 'Position id',
`name` varchar(100) NOT NULL                    COMMENT 'The name of the experience',
`description` varchar(100) NOT NULL             COMMENT 'Description of the experience',
`hyperlink` varchar(500) DEFAULT NULL           COMMENT 'Link for more information about the experience',
`start_date` date NOT NULL                      COMMENT 'The start of the experience',
`end_date` date DEFAULT NULL                    COMMENT 'The end of the experience',
PRIMARY KEY (`experience_id`),
FOREIGN KEY (`position_id`) REFERENCES `positions`(`position_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Experiences I have held";
