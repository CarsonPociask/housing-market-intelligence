CREATE DATABASE IF NOT EXISTS housing_intelligence;
USE housing_intelligence;

CREATE TABLE cities (
city_id  INT auto_increment PRIMARY KEY, 
city     VARCHAR(100) NOT NULL, 
state VARCHAR(2) NOT NULL,
UNIQUE KEY unique_city_state (city,state)
);

SHOW COLUMNS FROM cities;