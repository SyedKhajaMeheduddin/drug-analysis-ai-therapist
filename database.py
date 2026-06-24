import mysql.connector
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "drug_analysis_db"),
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    # Connect without db first to create it if needed
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cursor.execute(f"USE {DB_CONFIG['database']}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255),
            extracted_text TEXT,
            matched_drug VARCHAR(255),
            match_type VARCHAR(50),
            drug_info JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS therapy_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_concern TEXT,
            concern_category VARCHAR(100),
            ai_response TEXT,
            analysis_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE SET NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("[DB] Database initialized successfully.")
