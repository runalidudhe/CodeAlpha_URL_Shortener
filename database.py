
import sqlite3

DATABASE_NAME = "urls.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            clicks INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def save_url(short_code, original_url):
    conn = get_connection()

    conn.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
        (short_code, original_url)
    )

    conn.commit()
    conn.close()


def get_url(short_code):
    conn = get_connection()

    url = conn.execute(
        "SELECT * FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()
    return url


def update_clicks(short_code):
    conn = get_connection()

    conn.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
        (short_code,)
    )

    conn.commit()
    conn.close()


def get_all_urls():
    conn = get_connection()

    urls = conn.execute(
        "SELECT * FROM urls ORDER BY created_at DESC"
    ).fetchall()

    conn.close()
    return urls
