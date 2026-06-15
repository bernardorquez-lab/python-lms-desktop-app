import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "Database" / "danas_database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL UNIQUE,
        course_code TEXT NOT NULL UNIQUE,
        units TEXT,
        schedule TEXT,
        room TEXT,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        material_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        material_name TEXT,
        pdf_name TEXT,
        pdf_path TEXT,
        upload_date TEXT,
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database Ready!")