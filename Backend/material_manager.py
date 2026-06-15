import sqlite3
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "Database" / "danas_database.db"


def _connect():
    return sqlite3.connect(DB_PATH)


def add_material(course_id, material_name, pdf_name, pdf_path):
    conn = _connect()
    cursor = conn.cursor()

    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO materials (
            course_id,
            material_name,
            pdf_name,
            pdf_path,
            upload_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        course_id,
        material_name,
        pdf_name,
        pdf_path,
        upload_date
    ))

    conn.commit()
    conn.close()


def get_materials():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT material_id, course_id, material_name, pdf_name, pdf_path, upload_date
        FROM materials
        ORDER BY upload_date DESC
    """)

    materials = cursor.fetchall()

    conn.close()
    return materials


def get_materials_by_id(material_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM materials WHERE material_id = ?", (material_id,))

    material = cursor.fetchone()

    conn.close()
    return material


def get_materials_by_course(course_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT material_id, course_id, material_name, pdf_name, pdf_path, upload_date
        FROM materials
        WHERE course_id = ?
        ORDER BY upload_date DESC
    """, (course_id,))

    materials = cursor.fetchall()

    conn.close()
    return materials


def delete_material(material_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM materials WHERE material_id = ?", (material_id,))

    conn.commit()
    conn.close()


def get_material_count():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM materials")

    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_latest_materials():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pdf_name
        FROM materials
        ORDER BY material_id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()
    return result[0] if result else "No uploads found"