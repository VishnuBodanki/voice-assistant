import sqlite3
import os

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect("data/assistant.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, name):
    conn = sqlite3.connect("data/assistant.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", 
                       (username, password, name))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect("data/assistant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
