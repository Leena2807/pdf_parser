from flask import Flask
from flask_cors import CORS
from backend.routes.students import students_bp
from backend.pdf import pdf_bp


app = Flask(__name__)
CORS(app)

app.register_blueprint(students_bp)
app.register_blueprint(pdf_bp)


if __name__ == "__main__":
    app.run(debug=False)