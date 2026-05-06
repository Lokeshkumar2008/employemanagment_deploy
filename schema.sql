-- CREATE USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT,
    role TEXT
);

-- CREATE EMPLOYEE TABLE
CREATE TABLE IF NOT EXISTS employee (
    eid INTEGER PRIMARY KEY AUTOINCREMENT,
    ename TEXT,
    edept TEXT,
    email TEXT,
    esalary INTEGER,
    ephone TEXT
);
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
);

-- INSERT USER
INSERT INTO users (username, password, role)
VALUES ('lokesh', 'loki', 'hr');

-- INSERT EMPLOYEE
INSERT INTO employee (ename, edept, esalary, ephone)
VALUES ('mahe', 'bca', 25000, '1234567890');