import sqlite3
import hashlib
import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "Database" / "danas_database.db"

SENDER_EMAIL = "bernardorquez@gmail.com"      # ← replace this
SENDER_PASSWORD = "qbxm eudl lulp qiow"   # ← replace this

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role     TEXT NOT NULL DEFAULT 'student',
            email    TEXT
        );
    """)
    conn.commit()
    conn.close()
    migrate_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, username, password, email, role="student"):
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO users (name, username, password, email, role) VALUES (?, ?, ?, ?, ?)",
            (name, username, hash_password(password), email, role)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password))
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_email(email):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def update_password(username, new_password):
    conn = get_conn()
    conn.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (hash_password(new_password), username)
    )
    conn.commit()
    conn.close()

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(recipient_email, otp):
    msg = MIMEMultipart()
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = recipient_email
    msg["Subject"] = "DANAS - Your OTP Code"

    body = f"""
    Hello!

    Your OTP code for DANAS password reset is:

    {otp}

    This code is valid for this session only.
    Do not share it with anyone.

    - DANAS Team
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role     TEXT NOT NULL DEFAULT 'student',
            email    TEXT
        );
    """)
    conn.commit()
    conn.close()
    migrate_db()

def migrate_db():
    conn = get_conn()
    try:
        conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
        conn.commit()
    except:
        pass
    conn.close()