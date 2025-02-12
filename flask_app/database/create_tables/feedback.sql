CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each comment',
`name` varchar(100) NOT NULL                 COMMENT 'The commentator name',
`email` varchar(255) NOT NULL                COMMENT 'The commentator email',
`comment` text NOT NULL                      COMMENT 'The text of the comment',
PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="User feedback about the website";
