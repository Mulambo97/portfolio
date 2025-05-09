CREATE TABLE IF NOT EXISTS `skills` (
`skill_id` int(11) NOT NULL AUTO_INCREMENT                          COMMENT 'Identify  for each skill',
`experience_id` int(11) NOT NULL                                    COMMENT 'Experience id',
`name` varchar(100) NOT NULL                                        COMMENT 'The name of the skill',
`skill_level` int(11) NOT NULL CHECK (skill_level BETWEEN 1 AND 10) COMMENT 'The level of the skill (1-10)',
PRIMARY KEY (`skill_id`),
FOREIGN KEY (`experience_id`) REFERENCES `experiences`(`experience_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Skills associated with each experience";
