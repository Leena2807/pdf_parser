from flask import Blueprint, jsonify
from backend.db import get_db_connection

students_bp = Blueprint("students", __name__)

def insert_student(student):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO students
        (seat_number, name, sgpa_sem1, sgpa_sem2, result, source_file)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (seat_number)
        DO UPDATE SET
            name = EXCLUDED.name,
            sgpa_sem1 = EXCLUDED.sgpa_sem1,
            sgpa_sem2 = EXCLUDED.sgpa_sem2,
            result = EXCLUDED.result,
            source_file = EXCLUDED.source_file;
        """,
        (
            student["seat_number"],
            student["name"],
            student["sgpa_sem1"],
            student["sgpa_sem2"],
            student["result"],
            student["source_file"]
        )
    )

    conn.commit()
    cur.close()
    conn.close()

@students_bp.route("/search/<query>")
def search_students(query):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT seat_number, name, sgpa_sem1, sgpa_sem2, result, source_file
        FROM students
        WHERE name ILIKE %s
        """,
        (f"%{query}%",)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    students = [
        {
            "seat_number": r[0],
            "name": r[1],
            "sgpa_sem1": r[2],
            "sgpa_sem2": r[3],
            "result": r[4],
            "source_file": r[5]
        }
        for r in rows
    ]

    return jsonify(students)
@students_bp.route("/toppers")
def get_toppers():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT seat_number, name, sgpa_sem1, sgpa_sem2, result, source_file
        FROM students
        WHERE result = 'PASS'
        ORDER BY
            COALESCE(sgpa_sem2, sgpa_sem1) DESC
        LIMIT 3;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    toppers = [
        {
            "seat_number": r[0],
            "name": r[1],
            "sgpa_sem1": r[2],
            "sgpa_sem2": r[3],
            "result": r[4],
            "source_file": r[5]
        }
        for r in rows
    ]

    return jsonify(toppers)