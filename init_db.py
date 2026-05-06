import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("company.db")

# Create cursor
cursor = conn.cursor()

# ---------------- USERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT,
    role TEXT
)
""")

# ---------------- EMPLOYEE TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS employee (
    eid INTEGER PRIMARY KEY AUTOINCREMENT,
    ename TEXT,
    edept TEXT,
    email TEXT,
    esalary INTEGER,
    ephone TEXT
)
""")

# ---------------- INSERT DEFAULT USER ----------------
cursor.execute("""
INSERT INTO users (username, password, role)
VALUES ('lokesh', 'loki', 'hr')
""")

# ---------------- INSERT DEFAULT EMPLOYEE ----------------
cursor.execute("""
INSERT INTO employee (ename, edept, esalary, ephone)
VALUES ('mahe', 'bca', 25000, '1234567890')
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database and tables created successfully!")