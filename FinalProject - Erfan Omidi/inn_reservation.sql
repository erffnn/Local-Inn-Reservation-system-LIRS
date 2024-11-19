show databases;


CREATE DATABASE IF NOT EXISTS Inn_reservation;
drop database inn_reservation;
USE Inn_reservation;

CREATE TABLE inn_rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_type CHAR(1),
    room_price DECIMAL(5,2),
    availability SMALLINT
);

CREATE TABLE inn_customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(30),
    phone_number BIGINT UNIQUE
);

CREATE TABLE inn_reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_type INT,
    customer_id INT,
    accommodation_days SMALLINT,
    cost DECIMAL(5,2),
    checkout TINYINT DEFAULT 0,
    FOREIGN KEY (room_type) REFERENCES inn_rooms(id),
    FOREIGN KEY (customer_id) REFERENCES inn_customer(id)
);


INSERT INTO inn_rooms (room_type, room_price, availability) VALUES
('S', 100.00, 10),
('P', 150.00, 8),
('O', 200.00, 5),
('E', 80.00, 9);


INSERT INTO inn_customer (first_name, last_name, email, phone_number) VALUES
('Leo', 'Page', 'leo.page@gmail.com', 5141111110),
('Mike', 'Jackson', 'mike.jackson@gmail.com', 3651111110),
('Hiro', 'Mutto', 'hiro.mutto@gmail.com', 4321110000),
('Hiro', 'Mutto', 'hiro.mutto1@gmail.com', 43265432),
('Emma', 'Smith', 'emma.smith@gmail.com', 7259874321),
('Sophia', 'Johnson', 'sophia.johnson@gmail.com', 6247890123),
('Liam', 'Williams', 'liam.williams@gmail.com', 8176543210),
('Olivia', 'Jones', 'olivia.jones@gmail.com', 9365487120),
('Olivia', 'Jones', 'olivial.jones@gmail.com', 432456434),
('Noah', 'Brown', 'noah.brown@gmail.com', 2457896321),
('Ava', 'Davis', 'ava.davis@gmail.com', 7630147852),
('William', 'Miller', 'william.miller@gmail.com', 6314789023);


INSERT INTO inn_reservation (room_type, customer_id, accommodation_days, checkout) VALUES
(1, (SELECT id FROM inn_customer WHERE phone_number = 5141111110), 4, 0),
(2, (SELECT id FROM inn_customer WHERE phone_number = 3651111110), 2, 0),
(3, (SELECT id FROM inn_customer WHERE phone_number = 4321110000), 5, 0),
(4, (SELECT id FROM inn_customer WHERE phone_number = 43265432), 5, 0),
(1, (SELECT id FROM inn_customer WHERE phone_number = 7259874321), 6, 0),
(2, (SELECT id FROM inn_customer WHERE phone_number = 6247890123), 3, 0),
(3, (SELECT id FROM inn_customer WHERE phone_number = 8176543210), 7, 0),
(1, (SELECT id FROM inn_customer WHERE phone_number = 9365487120), 1, 0),
(4, (SELECT id FROM inn_customer WHERE phone_number = 432456434), 1, 0),
(2, (SELECT id FROM inn_customer WHERE phone_number = 2457896321), 9, 0),
(3, (SELECT id FROM inn_customer WHERE phone_number = 7630147852), 8, 0),
(1, (SELECT id FROM inn_customer WHERE phone_number = 6314789023), 2, 0);






















DROP TABLE IF EXISTS inn_customer;
DROP TABLE IF EXISTS inn_reservation;
DROP TABLE IF EXISTS inn_rooms;

SELECT * FROM inn_rooms;
select * from inn_customer;
SELECT * FROM inn_reservation;

