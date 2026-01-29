from flask import Blueprint, request, jsonify
import PyPDF2
from backend.routes.students import insert_student


from backend.parsers import (
    parse_ledger,
    parse_table_wrapped,
    parse_fe_single
)

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/add_pdf", methods=["POST"])
def add_pdf():
    files = request.files.getlist("file")
    if not files:
        return jsonify({"message": "No file uploaded"}), 400

    extracted = []

    for file in files:
        text = ""

        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t.upper() + "\n"

        # 🔍 FORMAT DETECTION
        if "COLLEGE LEDGER" in text:
            students = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    students.extend(
                        parse_ledger(page_text.upper(), file.filename)
                    )

        elif "STUDENT RESULT DATA" in text:
            students = parse_table_wrapped(text, file.filename)

        elif "FIRST SEMESTER SGPA" in text:
            students = parse_fe_single(text, file.filename)

        else:
            students = []

        extracted.extend(students)
        for s in students:
            insert_student(s)

    return jsonify({
        "students_extracted": len(extracted),
        "students": extracted
    }), 200