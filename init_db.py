import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("app.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        create_date TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        create_date TEXT NOT NULL,
        post_id INTEGER NOT NULL,
        FOREIGN KEY(post_id) REFERENCES posts(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized:", DB_PATH)
