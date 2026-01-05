-- SmartCampus Database Schema
-- Generated from SQLAlchemy Models

SET FOREIGN_KEY_CHECKS = 0;

-- --------------------------------------------------------
-- Table: user
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'Student'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: room
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS room (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    name VARCHAR(50) NOT NULL,
    building VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    equipment VARCHAR(200),
    room_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: booking
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS booking (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'Confirmed',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: maintenance_issue
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS maintenance_issue (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    room_id INT NOT NULL,
    reported_by_id INT NOT NULL,
    assigned_to_id INT,
    description TEXT NOT NULL,
    issue_type VARCHAR(50),
    priority VARCHAR(20) DEFAULT 'Medium',
    status VARCHAR(20) DEFAULT 'Open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE,
    FOREIGN KEY (reported_by_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to_id) REFERENCES user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: study_group
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS study_group (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    name VARCHAR(100) NOT NULL,
    module VARCHAR(50),
    description TEXT,
    created_by_id INT NOT NULL,
    FOREIGN KEY (created_by_id) REFERENCES user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: group_membership (Many-to-Many)
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS group_membership (
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES study_group(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: feedback
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: usage_data
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS usage_data (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    room_id INT NOT NULL UNIQUE,
    total_bookings INT DEFAULT 0,
    current_occupancy INT DEFAULT 0,
    utilization_rate FLOAT DEFAULT 0.0,
    FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
