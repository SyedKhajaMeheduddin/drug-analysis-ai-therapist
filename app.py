from flask import Flask
from modules.database import init_db
from routes.upload import upload_bp
from routes.drug import drug_bp
from routes.therapist import therapist_bp
from routes.admin import admin_bp
import os

app = Flask(__name__)
app.secret_key = "drug_analysis_secret_2025"
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.register_blueprint(upload_bp)
app.register_blueprint(drug_bp)
app.register_blueprint(therapist_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
