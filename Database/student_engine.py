import sqlite3
import hashlib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "Database" / "danas_database.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_enrollments_table() -> None:
    conn = _connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            course_id     INTEGER NOT NULL,
            enrolled_at   TEXT    NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id)   REFERENCES users(id)
                ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
                ON DELETE CASCADE,
            UNIQUE (user_id, course_id)
        )
    """)
    conn.commit()
    conn.close()


def get_user_profile(username: str) -> dict:
    conn = _connect()
    row = conn.execute(
        "SELECT id, name, username, role, email FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    if row is None:
        return {}

    return {
        "id":        row["id"],
        "full_name": row["name"],    
        "username":  row["username"],
        "role":      row["role"],
        "email":     row["email"] or "",
    }


def get_all_courses() -> list:
    conn = _connect()
    rows = conn.execute("""
        SELECT course_id,
               course_name  AS name,
               course_code  AS code,
               units,
               schedule,
               room,
               description
        FROM   courses
        ORDER  BY course_name
    """).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_student_courses(username: str) -> list:
    _ensure_enrollments_table()

    conn = _connect()
    rows = conn.execute("""
        SELECT c.course_id,
               c.course_name  AS name,
               c.course_code  AS code,
               c.units,
               c.schedule,
               c.room,
               c.description
        FROM   enrollments e
        JOIN   courses     c ON c.course_id = e.course_id
        JOIN   users       u ON u.id        = e.user_id
        WHERE  u.username = ?
        ORDER  BY c.course_name
    """, (username,)).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def enroll_student(username: str, course_code: str) -> bool:
    _ensure_enrollments_table()

    conn = _connect()
    try:
        user_row = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user_row is None:
            raise ValueError(f"No user found with username '{username}'.")

        course_row = conn.execute(
            "SELECT course_id FROM courses WHERE course_code = ?", (course_code,)
        ).fetchone()
        if course_row is None:
            raise ValueError(f"No course found with code '{course_code}'.")

        conn.execute(
            """
            INSERT INTO enrollments (user_id, course_id)
            VALUES (?, ?)
            """,
            (user_row["id"], course_row["course_id"])
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def unenroll_student(username: str, course_code: str) -> None:
    _ensure_enrollments_table()

    conn = _connect()
    try:
        conn.execute("""
            DELETE FROM enrollments
            WHERE user_id  = (SELECT id        FROM users   WHERE username    = ?)
              AND course_id = (SELECT course_id FROM courses WHERE course_code = ?)
        """, (username, course_code))
        conn.commit()
    finally:
        conn.close()


def get_course_materials(course_id: int) -> list:
    conn = _connect()
    rows = conn.execute("""
        SELECT material_id,
               course_id,
               material_name,
               pdf_name,
               pdf_path,
               upload_date
        FROM   materials
        WHERE  course_id = ?
        ORDER  BY upload_date DESC
    """, (course_id,)).fetchall()
    conn.close()

    return [dict(row) for row in rows]
