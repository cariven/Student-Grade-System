import sqlite3
import os


def get_db_path():
    return os.environ.get("DATABASE", "database.db")


def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            name       TEXT    NOT NULL,
            created_at TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            user_id    INTEGER NOT NULL,
            tugas      REAL    NOT NULL,
            uts        REAL    NOT NULL,
            uas        REAL    NOT NULL,
            final      REAL    NOT NULL,
            grade      TEXT    NOT NULL,
            created_at TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ── Users ─────────────────────────────────────────────────────────────────────

def insert_user(email, password_hash, created_at):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
        (email, password_hash, created_at),
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def fetch_user_by_email(email):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def fetch_user_by_id(user_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Students ──────────────────────────────────────────────────────────────────

def insert_student(user_id, name, created_at):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO students (user_id, name, created_at) VALUES (?, ?, ?)",
        (user_id, name, created_at),
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def fetch_all_students(user_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM students WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_student_by_id(student_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_student_by_id(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()


# ── Grades ────────────────────────────────────────────────────────────────────

def insert_grade(student_id, user_id, tugas, uts, uas, final, grade, created_at):
    conn = get_db_connection()
    cursor = conn.execute(
        """INSERT INTO grades
           (student_id, user_id, tugas, uts, uas, final, grade, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (student_id, user_id, tugas, uts, uas, final, grade, created_at),
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def fetch_grades_by_student(student_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM grades WHERE student_id = ? ORDER BY created_at DESC",
        (student_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_all_grades(user_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM grades WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_grade_by_id(grade_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
    conn.commit()
    conn.close()