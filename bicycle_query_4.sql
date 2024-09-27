-- Create the database and select it
CREATE DATABASE bicycle_rental;
USE bicycle_rental;

-- Create the users table
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the cycles table
CREATE TABLE cycles (
    cycle_id VARCHAR(10) PRIMARY KEY,
    status ENUM('Available', 'Not Available') DEFAULT 'Available',
    user_id VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Create the bookings table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    cycle_id VARCHAR(10) NOT NULL,
    rented_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_time TIMESTAMP NULL,
    rental_days INT NOT NULL,
    total_cost DECIMAL(5, 2) DEFAULT 0.00,
    overdue_status VARCHAR(50) DEFAULT 'On Time',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (cycle_id) REFERENCES cycles(cycle_id)
);

-- Insert initial cycle IDs CID001 to CID020
INSERT INTO cycles (cycle_id, status)
VALUES
('CID001', 'Available'),
('CID002', 'Available'),
('CID003', 'Available'),
('CID004', 'Available'),
('CID005', 'Available'),
('CID006', 'Available'),
('CID007', 'Available'),
('CID008', 'Available'),
('CID009', 'Available'),
('CID010', 'Available'),
('CID011', 'Available'),
('CID012', 'Available'),
('CID013', 'Available'),
('CID014', 'Available'),
('CID015', 'Available'),
('CID016', 'Available'),
('CID017', 'Available'),
('CID018', 'Available'),
('CID019', 'Available'),
('CID020', 'Available');

-- Insert admin user
INSERT INTO users (id, name, mobile_number, password, is_admin)
VALUES (UUID(), 'Gokul', '8124619546', SHA2('123456789', 256), TRUE);