CREATE DATABASE jobtrack;

USE jobtrack;

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    application_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL
);