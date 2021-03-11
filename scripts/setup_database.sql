CREATE DATABASE form990;

CREATE USER 'form990-dev'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT SELECT, UPDATE, INSERT, DELETE ON form990.* TO 'form990-dev'@'localhost';

CREATE USER 'form990-dev'@'%' IDENTIFIED BY '${DB_PASSWORD}';
GRANT SELECT, UPDATE, INSERT, DELETE ON from990.* TO 'form990-dev'@'%';

FLUSH PRIVILEGES;