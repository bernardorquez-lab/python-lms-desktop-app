import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "Database" / "danas_database.db"


def _connect():
    return sqlite3.connect(DB_PATH)


def add_course(name, code, units="", schedule="", room="", description=""):
    conn = _connect()

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM courses WHERE course_name = ?", (name,))
        name_exists = cursor.fetchone()

        cursor.execute("SELECT * FROM courses WHERE course_code = ?", (code,))
        code_exists = cursor.fetchone()

        if name_exists and code_exists:
            raise Exception("Course name and code already exist.")

        if name_exists:
            raise Exception("Course name already exists.")

        if code_exists:
            raise Exception("Course code already exists.")

        cursor.execute("""
            INSERT INTO courses (
                course_name,
                course_code,
                units,
                schedule,
                room,
                description
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (name, code, units, schedule, room, description))

        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_courses():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT course_id, course_name, course_code, units, schedule, room, description
        FROM courses
        ORDER BY course_name
    """)

    courses = cursor.fetchall()
    conn.close()
    return courses


def update_course(course_id, name, code, units="", schedule="", room="", description=""):
    conn = _connect()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM courses
            WHERE course_name = ?
            AND course_id != ?
            """,
            (name, course_id)
        )

        if cursor.fetchone():
            raise Exception("Course name already exists.")

        cursor.execute(
            """
            SELECT * FROM courses
            WHERE course_code = ?
            AND course_id != ?
            """,
            (code, course_id)
        )

        if cursor.fetchone():
            raise Exception("Course code already exists.")

        cursor.execute("""
            UPDATE courses
            SET course_name = ?,
                course_code = ?,
                units = ?,
                schedule = ?,
                room = ?,
                description = ?
            WHERE course_id = ?
        """, (name, code, units, schedule, room, description, course_id))

        conn.commit()
    finally:
        conn.close()


def delete_course(course_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM materials WHERE course_id = ?", (course_id,))
    cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))

    conn.commit()
    conn.close()


def get_course_count():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM courses")

    count = cursor.fetchone()[0]

    conn.close()
    return count