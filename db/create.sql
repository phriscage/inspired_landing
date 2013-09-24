## This file will create the necessary database schema and user for the application
#--create the database if not exist
CREATE DATABASE IF NOT EXISTS inspired_landing;
#--create the database if not exist
CREATE DATABASE IF NOT EXISTS inspired_landing_test;

#--create the user by explicit GRANT statements
GRANT ALL ON inspired_landing.* TO 'inspired_rw'@'localhost' IDENTIFIED BY PASSWORD '*69FDD7B25D8A20F7BBB9466607FE527B7ED372BF';
GRANT ALL ON inspired_landing.* TO 'inspired_rw'@'%' IDENTIFIED BY PASSWORD '*69FDD7B25D8A20F7BBB9466607FE527B7ED372BF';
FLUSH PRIVILEGES;

#--create the user by explicit GRANT statements
GRANT ALL ON inspired_landing_test.* TO 'inspired_rw'@'localhost' IDENTIFIED BY PASSWORD '*69FDD7B25D8A20F7BBB9466607FE527B7ED372BF';
GRANT ALL ON inspired_landing_test.* TO 'inspired_rw'@'%' IDENTIFIED BY PASSWORD '*69FDD7B25D8A20F7BBB9466607FE527B7ED372BF';
FLUSH PRIVILEGES;

