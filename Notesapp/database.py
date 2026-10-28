import os
import mysql.connector

# Support configured passwords with intelligent fallback
passwords = [os.environ.get('DB_PASSWORD'), 'root', 'Codegnan@25', '']
db = None

for pwd in passwords:
    if pwd is None:
        continue
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password=pwd,
            database='notes_app'
        )
        if db.is_connected():
            break
    except Exception:
        continue

if db is None:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Codegnan@25',
        database='notes_app'
    )

cursor = db.cursor()

# Auto-create tables if they don't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")
db.commit()