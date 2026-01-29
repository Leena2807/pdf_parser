

⸻

📄 PDF Result Parser

📌 Project Overview

PDF Result Parser is a backend-focused project that extracts student result data from university result PDFs and displays it in a structured tabular format.

The system is designed to handle different PDF result formats (single student, batch results, multi-page PDFs) and convert unstructured PDF text into clean, usable data.

⸻

🎯 What Problem It Solves

University result PDFs are:
	•	Unstructured
	•	Hard to query
	•	Different in format across semesters

This project automates:
	•	Reading result PDFs
	•	Extracting student details
	•	Presenting results in a structured table

⸻

⚙️ Features
	•	Upload result PDF(s)
	•	Automatically detect PDF format
	•	Extract:
	•	Seat Number
	•	Student Name
	•	SGPA (Semester-wise)
	•	Result Status (PASS / FAIL)
	•	Display extracted data in a table
	•	Supports:
	•	Single-student PDFs
	•	Batch result PDFs
	•	Multi-page PDFs

⸻

🧠 How It Works (Simple Flow)

PDF Upload
   ↓
Text Extraction (PyPDF2)
   ↓
Format Detection
   ↓
Custom Parser Logic
   ↓
Structured JSON
   ↓
Table Display


⸻

🛠️ Tech Stack
	•	Backend: Python, Flask
	•	PDF Processing: PyPDF2
	•	Regex: For pattern-based extraction
	•	Frontend: HTML, CSS, JavaScript
	•	Database (optional): PostgreSQL

⸻

📂 Project Structure

pdf_parser/
│
├── backend/
│   ├── app.py          # Flask app entry
│   ├── pdf.py          # PDF upload & parsing logic
│   ├── parsers.py      # Different PDF format parsers
│   ├── db.py           # Database connection
│   └── routes/
│       └── students.py # Search, toppers APIs
│
├── frontend/
│   ├── index.html
│   ├── index.js
│   └── styles.css
│
└── README.md


⸻

▶️ How to Run

1️⃣ Create virtual environment

python3 -m venv venv
source venv/bin/activate

2️⃣ Install dependencies

pip install flask flask-cors psycopg2 PyPDF2

3️⃣ Run backend

python3 -m backend.app

4️⃣ Open frontend

Open frontend/index.html in browser.

⸻

📥 Input
	•	PDF file containing university result data

📤 Output
	•	Table displaying extracted student results

⸻

🚀 Future Enhancements
	•	Advanced search & filtering
	•	Result analytics
	•	Support for more university formats
	•	Export to CSV / Excel

⸻

✅ Key Learning Outcomes
	•	Handling unstructured real-world data
	•	Regex-based parsing
	•	Backend architecture & clean separation
	•	Working with multiple input formats
	•	Building robust extraction pipelines

