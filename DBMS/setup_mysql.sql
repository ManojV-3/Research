-- ═══════════════════════════════════════════════════════════
-- ResearchVault - MySQL Database Setup Script
-- Run this ONCE to create the database and user
-- ═══════════════════════════════════════════════════════════

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS research_pub
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE research_pub;

-- 2. Create a dedicated user (change password before production!)
CREATE USER IF NOT EXISTS 'research_user'@'localhost'
  IDENTIFIED BY 'ResearchVault@2024';

GRANT ALL PRIVILEGES ON research_pub.* TO 'research_user'@'localhost';
FLUSH PRIVILEGES;

-- 3. Tables (Flask-SQLAlchemy also auto-creates these via db.create_all())

CREATE TABLE IF NOT EXISTS faculty (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(150) NOT NULL,
    designation      VARCHAR(100) NOT NULL,
    department       VARCHAR(150) NOT NULL,
    year_of_joining  INT          NOT NULL,
    email            VARCHAR(200) NOT NULL UNIQUE,
    created_at       DATETIME     DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS publication (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id       INT          NOT NULL,
    title            VARCHAR(500) NOT NULL,
    pub_type         ENUM('journal','conference','book_chapter','book') NOT NULL,
    publication_name VARCHAR(300) NOT NULL,
    issn_isbn        VARCHAR(50),
    pub_year         INT          NOT NULL,
    pub_month        VARCHAR(20)  NOT NULL,
    doi              VARCHAR(200),
    created_at       DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE,
    INDEX idx_faculty (faculty_id),
    INDEX idx_year    (pub_year),
    INDEX idx_type    (pub_type)
) ENGINE=InnoDB;

-- ═══════════════════════════════════════════════════════════
-- Sample seed data (optional – remove for fresh install)
-- ═══════════════════════════════════════════════════════════

INSERT IGNORE INTO faculty (name, designation, department, year_of_joining, email) VALUES
('Dr. Anita Sharma',   'Professor',           'Computer Science & Engineering', 2015, 'anita.sharma@university.edu'),
('Dr. Rajesh Kumar',   'Associate Professor', 'Electronics & Communication',    2018, 'rajesh.kumar@university.edu'),
('Dr. Priya Nair',     'Assistant Professor', 'Mathematics',                    2020, 'priya.nair@university.edu');

INSERT IGNORE INTO publication
  (faculty_id, title, pub_type, publication_name, issn_isbn, pub_year, pub_month, doi)
SELECT f.id,
  'Deep Learning Approaches for Medical Image Segmentation',
  'journal', 'IEEE Transactions on Medical Imaging', '0278-0062', 2023, 'August',
  '10.1109/TMI.2023.1234567'
FROM faculty f WHERE f.email = 'anita.sharma@university.edu';

INSERT IGNORE INTO publication
  (faculty_id, title, pub_type, publication_name, issn_isbn, pub_year, pub_month, doi)
SELECT f.id,
  'Optimizing OFDM Systems Using Reinforcement Learning',
  'conference', 'IEEE International Conference on Communications (ICC)', '978-1-7281-5151-1',
  2023, 'May', '10.1109/ICC45855.2023.9876543'
FROM faculty f WHERE f.email = 'rajesh.kumar@university.edu';

INSERT IGNORE INTO publication
  (faculty_id, title, pub_type, publication_name, issn_isbn, pub_year, pub_month, doi)
SELECT f.id,
  'Graph Theory Applications in Network Security',
  'book_chapter', 'Advances in Cybersecurity: Theory and Practice', '978-0-12-345678-9',
  2022, 'November', NULL
FROM faculty f WHERE f.email = 'priya.nair@university.edu';
