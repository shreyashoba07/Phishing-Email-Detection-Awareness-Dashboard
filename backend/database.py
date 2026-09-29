import sqlite3


DATABASE_NAME = "backend/phishing_analysis.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            risk_score REAL,
            classification TEXT,
            ml_classification TEXT,
            phishing_probability REAL,
            recommendation TEXT
        )
    """)

    connection.commit()
    connection.close()