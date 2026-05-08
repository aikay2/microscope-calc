# database.py

import sqlite3

DB_NAME = "microscope.db"

# -----------------------------
# Connect to DB
# -----------------------------
def connect():
    return sqlite3.connect(DB_NAME)

# -----------------------------
# Create table
# -----------------------------
def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        measured_size REAL NOT NULL,
        real_size REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# Insert record
# -----------------------------
def insert_record(username, measured_size, real_size):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO records (username, measured_size, real_size)
    VALUES (?, ?, ?)
    """, (username, measured_size, real_size))

    conn.commit()
    conn.close()

# -----------------------------
# View all records
# -----------------------------
def view_records():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()

    conn.close()
    return records

# -----------------------------
# Delete record
# -----------------------------
def delete_record(record_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))

    conn.commit()
    conn.close()
