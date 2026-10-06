CREATE DATABASE IF NOT EXISTS contact_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE contact_management;

CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255),
    category VARCHAR(50) NOT NULL DEFAULT 'Other',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional sample data for testing.
INSERT INTO contacts (name, phone, email, address, category) VALUES
('Rahul Shah', '9876543210', 'rahul@example.com', 'Vadodara, Gujarat', 'Friend'),
('Priya Patel', '9123456780', 'priya@example.com', 'Ahmedabad, Gujarat', 'College'),
('Amit Kumar', '9988776655', 'amit@example.com', 'Surat, Gujarat', 'Work');
